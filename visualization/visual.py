from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.offline import plot
from plotly.subplots import make_subplots
from data.getdata.mysql import data_load


# ---- 1페이지 시작 ---- #

# 공공도서관 수
def intro_map():
    df_libraries = data_load('gu_libraries')
    df_libraries.set_index('자치구', inplace=True)
    df_libraries.drop(['2017', '2018', '2020', '2021'], axis=1, inplace=True)
    df_libraries.rename({'2019': '도서관'}, axis=1, inplace=True)
    df_libraries = df_libraries.astype({'도서관': 'int'})

    seoul_geo = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'
    fig = px.choropleth(df_libraries, geojson=seoul_geo, locations=df_libraries.index, featureidkey='properties.name',
                        color='도서관', color_continuous_scale='Blues')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_coloraxes(showscale=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    plot_div = plot(fig, output_type='div')
    return plot_div


# 대출자 연령대
def rent_ages():
    df_rent = data_load("library_rent")
    df_rent = df_rent[df_rent['연도'] == '2019']
    ages_rent = list()
    ages_rent.append(df_rent['어린이회원'].sum())
    ages_rent.append(df_rent['청소년회원'].sum())
    ages_rent.append(df_rent['성인회원'].sum())

    labels = ['어린이', '청소년', '성인']
    values = ages_rent
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title={'text': '연령대별 공공도서관 대출 회원 수', 'font_size': 18, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'})
    fig.update_traces(textposition='inside', textinfo='label+percent', hovertemplate=None, hoverinfo='skip')
    fig.update_layout(showlegend=False)

    plot_div = plot(fig, output_type='div')
    return plot_div


# 공공도서관 예산
def gu_lib_budget():
    df_budget = data_load('gu_librarybudget')
    mask = (df_budget['연도'] == '2019')
    df_budget = df_budget[mask]
    df_budget.set_index('자치구', inplace=True)
    df_budget.sort_values(by='예산', ascending=False, inplace=True)

    fig = go.Figure(data=go.Bar(x=df_budget.index, y=df_budget['예산']),
                    layout=go.Layout(title='자치구별 예산', template='plotly_white'))
    fig.update_traces(hovertemplate='%{x}: %{y:.0f}만원<extra></extra>')

    plot_div = plot(fig, output_type='div')
    return plot_div

# ---- 1페이지 끝 ---- #


# ---- 2페이지 시작 ---- #

# 평균 소득과 도서관 수
def income_lib():
    gu_libraries = data_load('gu_libraries')
    gu_averageincome = data_load('gu_averageincome')
    df_income_lib = pd.merge(left=gu_libraries, right=gu_averageincome, how="inner", on="자치구")
    df_income_lib.drop(['2017_x', '2018_x', '2020_x', '2021', '2017_y', '2018_y', '2020_y'], axis=1, inplace=True)
    df_income_lib.columns = ['자치구', '도서관', '평균소득']
    df_income_lib.set_index('자치구', inplace=True)
    df_income_lib['평균소득'] = df_income_lib['평균소득'] / 10000

    fig = px.scatter(df_income_lib, x='평균소득', y='도서관', color='도서관', size='평균소득',
                     color_continuous_scale='blugrn', template='plotly_white')
    fig.update_layout(title={'text': '자치구별 평균소득과 도서관 수', 'font_size': 18, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'})
    fig.update_traces(hovertemplate='<b>%{text}</b><br>평균 소득: %{x:.1f}만원<br>도서관: %{y}개', text=df_income_lib.index)

    plot_div = plot(fig, output_type='div')
    return plot_div


# 도서관 수와 생활 만족도 (사회환경)
def satisfaction():
    # 2017년에서 2019년의 사회환경 만족도 변화율 -> 도서관이 증가한 구만 선택
    df = data_load('gu_satisfaction')
    df.set_index('자치구', inplace=True)
    df_sat = df[df['연도'] == '2019']['사회환경'] / df[df['연도'] == '2017']['사회환경'] * 100 - 100
    df_sat = df_sat.loc[['강남구', '노원구', '동대문구', '동작구', '서초구', '성북구', '양천구', '은평구', '종로구', '중랑구']]

    fig = px.bar(df_sat, x=df_sat.index, y=df_sat.values)
    fig.update_layout(
        title={'text': "도서관이 증가한 자치구의 생활 만족도 변화 (2017 → 2019)", 'font_size': 18, 'y': 0.95, 'x': 0.5,
               'xanchor': 'center', 'yanchor': 'top'},
        xaxis_title="자치구", yaxis_title="만족도 증감", template='plotly_white')
    fig.update_traces(hovertemplate='%{x}<br>%{y}%')
    fig.add_hline(y=0)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(visible=False, showticklabels=False)

    plot_div = plot(fig, output_type='div')
    return plot_div


# 1인 평균 도서관 방문 수
def lib_visitor():
    library_users = data_load('library_users')
    library_users = library_users[library_users['연도'] == '2019'].groupby('자치구').sum()
    library_users.index.name = '자치구'

    library_rent = data_load('library_rent').groupby('자치구').sum()
    library_rent['대출자수'] = library_rent.sum(axis=1)

    gu_youth_population = data_load('gu_youth_population')
    gu_youth_population = gu_youth_population[gu_youth_population['연도'] == '2019']
    gu_youth_population.set_index('자치구', inplace=True)

    df_visitor = pd.merge(left=library_users['방문자수'], right=library_rent['대출자수'], how="inner", on="자치구")
    df_visitor = pd.merge(left=df_visitor, right=gu_youth_population['총인구'], how="inner", on="자치구")
    df_visitor['1인당방문수'] = df_visitor['방문자수'] / df_visitor['총인구']
    df_visitor.sort_values(by='1인당방문수', inplace=True, ascending=False)

    colors = ['skyblue', ] * 25
    for i in range(5):
        colors[i] = 'yellowgreen'

    fig = go.Figure(data=[go.Bar(x=df_visitor.index, y=df_visitor['1인당방문수'], marker_color=colors)])
    fig.update_layout(title={'text': '1인 평균 도서관 방문 수 (2019)', 'font_size': 18, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'}, template='plotly_white')
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_traces(hovertemplate='%{x}: 평균 %{y:.1f}회<extra></extra>')

    plot_div = plot(fig, output_type='div')
    return plot_div


# 학령인구와 방문자수

# 인구 대비 방문자수

# 방문자가 많은 구의 연령대 비율
def age_percent():
    library_users = data_load('library_users')
    library_users = library_users[library_users['연도'] == '2019'].groupby('자치구').sum()
    library_users.index.name = '자치구'

    gu_youth_population = data_load('gu_youth_population')
    gu_youth_population = gu_youth_population[gu_youth_population['연도'] == '2019']
    gu_youth_population.set_index('자치구', inplace=True)

    df_visitor = pd.merge(left=library_users['방문자수'], right=gu_youth_population['총인구'], how="inner", on="자치구")
    df_visitor['1인당방문수'] = df_visitor['방문자수'] / df_visitor['총인구']
    df_visitor.sort_values(by='1인당방문수', inplace=True, ascending=False)

    gu_index = list(df_visitor.index[:5])
    gu_ages = data_load('gu_ages')
    gu_ages.set_index('자치구', inplace=True)
    gu_ages.rename(columns={'10이하': '10대이하'}, inplace=True)
    df_age_filter = gu_ages.loc[gu_index]

    labels = ['10대이하', '2030대', '4050대', '60이상']
    fig = px.bar(df_age_filter, x=labels, y=df_age_filter.index, title="자치구별 연령대 인구",
                 template='plotly_white', orientation='h',
                 color_discrete_map={'10대이하': 'lightgreen', '2030대': 'aquamarine',
                                     '4050대': 'cornflowerblue', '60이상': 'slateblue'})
    fig.update_layout(title={'text': '도서관 방문자가 많은 구의 연령대 비율', 'font_size': 18, 'y': 0.95, 'x': 0.5,
                             'xanchor': 'center', 'yanchor': 'top'}, xaxis=dict(title="인구 수", tickformat=','))
    fig.update_traces(hovertemplate='%{x:.0f}명<extra></extra>')

    plot_div = plot(fig, output_type='div')
    return plot_div



# ---- 3페이지 ---- #

# (시각화X) 취약계층 자료 데이터프레임
def df_disadv():
    df_income = data_load('gu_averageincome')
    df_income.drop(['2017', '2018', '2020'], axis=1, inplace=True)
    df_income.set_index('자치구', inplace=True)
    df_income.columns = ['소득']
    df_income['소득'] = df_income['소득'] / 10000  # 숫자가 너무 길어서 10000으로 나눔

    df_budget = data_load('gu_disadv_budget')
    df_users = data_load('gu_disadv_users')
    df_disadv_pre = pd.merge(left=df_budget, right=df_users, how="inner", on="자치구")
    df_disadv_pre.set_index('자치구', inplace=True)
    df_disadv_pre.drop(['2017', '2018'], axis=1, inplace=True)
    df_disadv_pre.columns = ['총예산', '이용자']

    df_libs = data_load('gu_libraries')
    df_libs.drop(['2017', '2018', '2020', '2021'], axis=1, inplace=True)
    df_libs.set_index('자치구', inplace=True)
    df_libs.columns = ['도서관']
    df_disadv = pd.concat([df_income, df_disadv_pre, df_libs], axis=1)

    return df_disadv


# 상관관계 히트맵
def corr_heatmap():
    corr = df_disadv().corr(method='pearson')
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    corr_mask = corr.mask(mask)

    fig = px.imshow(corr_mask, text_auto=True, color_continuous_scale='Rdbu', range_color=(-1, 1),
                    template='plotly_white')
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_traces(hovertemplate=None, hoverinfo='skip')

    plot_div = plot(fig, output_type='div')
    return plot_div


# 취약계층 총 예산과 취약계층 이용자 수
def disadv_budget_users():
    # pip install statsmodels
    df = df_disadv()
    fig = px.scatter(df, x='총예산', y='이용자', size='총예산', color='이용자', color_continuous_scale='Blugrn',
                     template="plotly_white", trendline="ols", trendline_color_override='yellow')
    fig.update_layout(
        title={'text': "서울시 자치구별 취약계층 예산과 도서관 이용자 수 비교 (2019)", 'font_size': 18, 'y': 0.95, 'x': 0.5,
               'xanchor': 'center', 'yanchor': 'top'},
        xaxis_title="총 예산(만 원)", yaxis_title="이용자 수(명)")
    fig.update_traces(hovertemplate='<b>%{text}</b><br>총 예산: %{x:.1f}만원<br>이용자: %{y:.1f}명', text=df_disadv().index)
    fig.update_layout(showlegend=False)
    fig.update_coloraxes(showscale=False)

    plot_div = plot(fig, output_type='div')
    return plot_div


# 취약계층 평균 예산과 평균 소득
def disadv_av_budget_income():
    df = df_disadv().sort_values(by='소득', ascending=False)
    df['1관당예산'] = df['총예산'] / df['도서관']

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df.index, y=df['소득'], width=0.5, marker_color='orange',
                         hovertemplate='%{x} 평균 소득:<br>%{y:$.1f}만원<extra></extra>'), secondary_y=False)
    fig.add_trace(
        go.Bar(x=df.index, y=df['1관당예산'], offset=0.01, width=0.5, marker_color='turquoise', opacity=0.8,
               hovertemplate='%{x} 평균 예산:<br>%{y:$.1f}만원<extra></extra>'), secondary_y=True)

    fig.update_layout(barmode='group', template='plotly_white', showlegend=False,
                      title={'text': "서울시 자치구별 취약계층 예산과 구 평균 소득 비교 (2019)", 'font_size': 18,
                             'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
    fig.update_yaxes(title_text="구 평균 소득 (만 원)", secondary_y=False)
    fig.update_yaxes(title_text="도서관 1관당 취약계층 예산 (만 원)", secondary_y=True)

    plot_div = plot(fig, output_type='div')
    return plot_div

# ---- 3페이지 끝 ---- #
