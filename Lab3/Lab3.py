from spyre import server
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('../df.csv')
df = pd.DataFrame(data)

area_names = {
    "1": "Vinnytsia r.",
    "2": "Volyn r.",
    "3": "Dnipro r.",
    "4": "Donetsk r.",
    "5": "Zhytomyr r.",
    "6": "Zakarpattia r.",
    "7": "Zaporizhzhia r.",
    "8": "Ivano-Frankivsk r.",
    "9": "Kyiv r.",
    "10": "Kirovohrad r.",
    "11": "Luhansk r.",
    "12": "Lviv r.",
    "13": "Mykolaiv r.",
    "14": "Odesa r.",
    "15": "Poltava r.",
    "16": "Rivne r.",
    "17": "Sumy r.",
    "18": "Ternopil r.",
    "19": "Kharkiv r.",
    "20": "Kherson r.",
    "21": "Khmelnytshyi r.",
    "22": "Cherkasy r.",
    "23": "Chernivtsi r.",
    "24": "Chernihiv r.",
    "25": "AR Crimea",
    "26": "Kyiv c.",
    "27": "Sevastopol c."
}

class VHIApp(server.App):
    title = "NOAA data visualisation"

    inputs = [
        {
            "type": "dropdown",
            "label": "Оберіть індекс",
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"},
            ],
            "key": "index_key",
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "label": "Оберіть область",
            "options": [{"label": name, "value": key} for key, name in area_names.items()],
            "value": 26,
            "key": "area_key",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "label": "Інтервал тижнів",
            "key": "range_weeks",
            "value": "9-10",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "label": "Інтервал років",
            "key": "range_years",
            "value": "1982-1988",
            "action_id": "update_data"
        }
    ]

    controls = [
        {
            'type': 'button',
            'id': 'update_data',
            'label': 'Show data'
        }]

    tabs = ["Table", "Plot"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot",
            "on_page_load": True
        },
        {
            "type": "table",
            "id": "data_table",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        index = params["index_key"]
        area = int(params["area_key"])
        week_range = params["range_weeks"]
        year_range = params["range_years"]

        start_week, end_week = map(int, week_range.split('-'))

        start_year, end_year = map(int, year_range.split('-'))

        filtered_df = df[
            (df["area"] == area) &
            (df["Year"] >= start_year) & (df["Year"] <= end_year) &
            (df["Week"] >= start_week) & (df["Week"] <= end_week)
            ]

        filtered_df = filtered_df[["Year", "Week", index]]
        return filtered_df

    def getPlot(self, params):
        area = int(params['area_key'])
        start_year, end_year = map(int, params['range_years'].split('-'))
        start_week, end_week = map(int, params['range_weeks'].split('-'))

        filtered_df = df[
            (df['area'] == area) &
            (df['Year'] >= start_year) & (df['Year'] <= end_year) &
            (df['Week'] >= start_week) & (df['Week'] <= end_week)
            ]

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.lineplot(x='Year', y=params['index_key'], ax=ax, data=filtered_df, color='purple', marker='o')

        ax.grid()
        area_name = area_names[str(params['area_key'])]
        ax.set_title(f'{params["index_key"]} для {area_name}')
        ax.set_xlabel('Рік')
        ax.set_ylabel(params['index_key'])

        return ax.get_figure()

app = VHIApp()
app.launch(port=9093)
