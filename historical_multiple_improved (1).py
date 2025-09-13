import flet as ft
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np

def get_stock_data(ticker):
    ticker = ticker.replace(" ", "")  
    if ticker[-1].isdigit():
        formats_to_try = [f"{ticker}.SA", ticker[:-1], f"{ticker[:-1]}4.SA" if ticker.endswith('3') else f"{ticker[:-1]}3.SA"]
    else:
        formats_to_try = [ticker, f"{ticker}3.SA", f"{ticker}4.SA"]

    for format_ticker in formats_to_try:
        data = yf.download(format_ticker, period="max", interval="1d", auto_adjust=False, multi_level_index=False)
        if not data.empty:
            return data, format_ticker

    return None, ticker

def calculate_future_returns(data, periods=[180, 360]):
    future_returns = pd.DataFrame(index=data.index)
    for period in periods:
        future_returns[f'Return_{period}d'] = data['Adj Close'].pct_change(periods=period).shift(-period)
    return future_returns

def analyze_historical_multiples(combined_df, periods=[180, 360]):
    thresholds = np.linspace(combined_df['Historical Multiple'].min(), combined_df['Historical Multiple'].max(), 50)
    results = []
    for threshold in thresholds:
        filtered_data = combined_df[combined_df['Historical Multiple'] <= threshold]
        row = [threshold]
        for period in periods:
            median_return = filtered_data[f'Return_{period}d'].median()
            row.append(median_return)
        results.append(row)
    results = pd.DataFrame(results, columns=['Threshold'] + [f'Median Return {period}d' for period in periods])
    best_thresholds = {}
    for period in periods:
        best_threshold = results.loc[results[f'Median Return {period}d'].idxmax()]
        best_thresholds[period] = (best_threshold['Threshold'], best_threshold[f'Median Return {period}d'])
    return best_thresholds

def main(page: ft.Page):
    page.title = "Historical Multiple App"
    page.theme_mode = ft.ThemeMode.DARK
    page.background_color = "#1E1E2D"
    page.favicon = "favicon.jpg"
    
    def fetch_data(e):
        ticker = ticker_input.value
        data, valid_ticker = get_stock_data(ticker)
        
        if data is None:
            scrollable_results.content = ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED_400, size=48),
                            ft.Text("Ticker não encontrado", 
                                   size=18, 
                                   weight=ft.FontWeight.W_500,
                                   color=ft.Colors.RED_400,
                                   text_align=ft.TextAlign.CENTER)
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=16),
                        padding=40,
                        alignment=ft.alignment.center
                    ),
                    elevation=8,
                    color="#2A2A3E"
                ),
                padding=20
            )
        else:
            stock_info = yf.Ticker(valid_ticker)
            company_name = stock_info.info.get('longName', 'Company name not available')
            currency = stock_info.info.get('currency', 'USD')
            data["MA50"] = data["Close"].rolling(window=50, min_periods=1).mean()
            current_date = datetime.now().strftime('%Y-%m-%d')
            last_close_price = data['Adj Close'].iloc[-1]
            last_ma50 = data['MA50'].iloc[-1]
            historical_multiple = last_close_price / last_ma50
            historical_multiples = data['Adj Close'][49:] / data['MA50'][49:]
            global_historical_multiple = historical_multiples.mean()
            higher_count = (historical_multiples > historical_multiple).sum()
            higher_than_today = (higher_count / len(historical_multiples)) * 100
            currency_symbol = "BRL" if currency == "BRL" else "USD"
            future_returns = calculate_future_returns(data)
            historical_multiples_df = historical_multiples.reset_index()
            historical_multiples_df.columns = ['Date', 'Historical Multiple']
            historical_multiples_df['Date'] = pd.to_datetime(historical_multiples_df['Date'])
            historical_multiples_df.set_index('Date', inplace=True)
            combined_df = historical_multiples_df.join(future_returns)
            best_thresholds = analyze_historical_multiples(combined_df)
            
            scrollable_results.content = ft.Container(
                content=ft.Column([
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.TRENDING_UP, color=ft.Colors.BLUE_400, size=32),
                                    ft.Column([
                                        ft.Text(ticker.upper(), 
                                               size=24, 
                                               weight=ft.FontWeight.BOLD,
                                               color=ft.Colors.WHITE),
                                        ft.Text(company_name, 
                                               size=14, 
                                               color=ft.Colors.GREY_400)
                                    ], spacing=2, expand=True)
                                ], alignment=ft.MainAxisAlignment.START),
                                ft.Divider(color=ft.Colors.GREY_600, height=1),
                                ft.Text(f"Data atual: {current_date}", 
                                       size=12, 
                                       color=ft.Colors.GREY_400)
                            ], spacing=12),
                            padding=20
                        ),
                        elevation=8,
                        color="#2A2A3E"
                    ),
                    
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text("Informações de Preço", 
                                       size=18, 
                                       weight=ft.FontWeight.W_600,
                                       color=ft.Colors.WHITE),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Preço Atual", 
                                                   size=12, 
                                                   color=ft.Colors.GREY_400),
                                            ft.Text(f"{last_close_price:.2f} {currency_symbol}", 
                                                   size=20, 
                                                   weight=ft.FontWeight.BOLD,
                                                   color=ft.Colors.GREEN_400)
                                        ], spacing=4),
                                        expand=True
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Média 50 dias", 
                                                   size=12, 
                                                   color=ft.Colors.GREY_400),
                                            ft.Text(f"{last_ma50:.2f} {currency_symbol}", 
                                                   size=20, 
                                                   weight=ft.FontWeight.BOLD,
                                                   color=ft.Colors.BLUE_400)
                                        ], spacing=4),
                                        expand=True
                                    )
                                ])
                            ], spacing=16),
                            padding=20
                        ),
                        elevation=8,
                        color="#2A2A3E"
                    ),
                    
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text("Análise do Historical Multiple", 
                                       size=18, 
                                       weight=ft.FontWeight.W_600,
                                       color=ft.Colors.WHITE),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Atual", 
                                                   size=12, 
                                                   color=ft.Colors.GREY_400),
                                            ft.Text(f"{historical_multiple:.2f}", 
                                                   size=24, 
                                                   weight=ft.FontWeight.BOLD,
                                                   color=ft.Colors.ORANGE_400)
                                        ], spacing=4),
                                        expand=True
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Média Histórica", 
                                                   size=12, 
                                                   color=ft.Colors.GREY_400),
                                            ft.Text(f"{global_historical_multiple:.2f}", 
                                                   size=24, 
                                                   weight=ft.FontWeight.BOLD,
                                                   color=ft.Colors.PURPLE_400)
                                        ], spacing=4),
                                        expand=True
                                    )
                                ]),
                                ft.Container(
                                    content=ft.Text(
                                        f"Historical Multiple tem sido historicamente mais alto do que o valor atual em {higher_than_today:.2f}% das vezes.",
                                        size=14,
                                        color=ft.Colors.GREY_300,
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    padding=ft.padding.only(top=16)
                                )
                            ], spacing=16),
                            padding=20
                        ),
                        elevation=8,
                        color="#2A2A3E"
                    ),
                    
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color=ft.Colors.YELLOW_400, size=24),
                                    ft.Text("Recomendações de Compra", 
                                           size=18, 
                                           weight=ft.FontWeight.W_600,
                                           color=ft.Colors.WHITE)
                                ]),
                                *[
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Row([
                                                ft.Container(
                                                    content=ft.Text(f"{period}d", 
                                                                   size=12, 
                                                                   weight=ft.FontWeight.BOLD,
                                                                   color=ft.Colors.WHITE),
                                                    bgcolor=ft.Colors.INDIGO_600,
                                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                                    border_radius=12
                                                ),
                                                ft.Text(f"Retorno: {best_thresholds[period][1]:.2%}", 
                                                       size=14, 
                                                       weight=ft.FontWeight.W_500,
                                                       color=ft.Colors.GREEN_400)
                                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.Text(
                                                f"Melhor compra abaixo de {best_thresholds[period][0]:.2f}",
                                                size=13,
                                                color=ft.Colors.GREY_300
                                            )
                                        ], spacing=8),
                                        padding=16,
                                        bgcolor="#1A1A2E",
                                        border_radius=8,
                                        border=ft.border.all(1, ft.Colors.GREY_700)
                                    ) for period in [180, 360]
                                ]
                            ], spacing=16),
                            padding=20
                        ),
                        elevation=8,
                        color="#2A2A3E"
                    )
                ], spacing=16),
                padding=20
            )
        
        page.update()
    
    ticker_input = ft.TextField(label="Digite o ticker da ação (Exemplo: AAPL):")
    fetch_button = ft.ElevatedButton(text="Buscar Ação", on_click=fetch_data)
    
    results_container = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.SEARCH, color=ft.Colors.GREY_600, size=64),
                ft.Text("Digite um ticker e clique em 'Buscar Ação' para ver os resultados", 
                       size=16, 
                       color=ft.Colors.GREY_500,
                       text_align=ft.TextAlign.CENTER)
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16),
            padding=40,
            alignment=ft.alignment.center
        ),
        expand=True
    )

    scrollable_results = ft.Container(
        content=results_container,
        expand=True,
        padding=ft.padding.only(bottom=20)
    )

    main_column = ft.Column(
        controls=[
            ft.Container(
                content=ft.Column([
                    ticker_input,
                    ft.Container(content=fetch_button, alignment=ft.alignment.center)
                ], spacing=20),
                padding=ft.padding.only(bottom=20)
            ),
            ft.Container(
                content=scrollable_results,
                expand=True
            )
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )
    
    page.add(main_column)

ft.app(target=main, view=ft.AppView.FLET_APP)

