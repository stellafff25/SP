import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Завантаження даних
def load_data():
    data = pd.read_csv('data.csv')
    return data

# Фільтрація даних
def filter_data(data, area, years, weeks):
    return data[
        (data['area'] == area) &
        (data['Year'].between(years[0], years[1])) &
        (data['Week'].between(weeks[0], weeks[1]))
    ]

# Основний додаток
def main():
    st.title("Аналіз індексів VCI, TCI та VHI")

    # Завантаження даних
    data = load_data()
    if data is None:
        st.stop()

    # Заміна кодів area на назви областей
    data['area'] = data['area'].astype(str)
    data['area_name'] = data['area'].map(area_names)

    # Початкові значення для фільтрів
    default_index = "VCI"
    default_area = list(area_names.values())[6]
    default_year_range = (1988, 2002)
    default_week_range = (9, 10)

    # Ініціалізація значень
    st.session_state.selected_index = default_index
    st.session_state.selected_area = default_area
    st.session_state.year_range = default_year_range
    st.session_state.week_range = default_week_range

    # Дві колонки для фільтрів і графіка
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Фільтри")

        # Кнопка скидання
        if st.button("Скинути фільтри"):
            st.session_state.selected_index = default_index
            st.session_state.selected_area = default_area
            st.session_state.year_range = default_year_range
            st.session_state.week_range = default_week_range

        # Компоненти фільтрів
        st.session_state.selected_index = st.selectbox(
            "Оберіть індекс", ["VCI", "TCI", "VHI"], index=["VCI", "TCI", "VHI"].index(st.session_state.selected_index)
        )
        st.session_state.selected_area = st.selectbox(
            "Оберіть область", options=list(area_names.values()), index=list(area_names.values()).index(st.session_state.selected_area)
        )
        selected_area_code = [k for k, v in area_names.items() if v == st.session_state.selected_area][0]
        st.session_state.year_range = st.slider(
            "Виберіть інтервал років", int(data['Year'].min()), int(data['Year'].max()), st.session_state.year_range
        )
        st.session_state.week_range = st.slider(
            "Виберіть інтервал тижнів", 1, 52, st.session_state.week_range
        )

    # Фільтровані дані
    filtered_data = filter_data(data, selected_area_code, st.session_state.year_range, st.session_state.week_range)

    # Вкладки для графіка і таблиці
    with col2:
        tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік 1", "Графік 2"])

        with tab1:
            st.header("Таблиця")

            # Вибір індексу з випадаючого списку
            selected_index = st.session_state.selected_index

            # Фільтруємо дані для вибраного індексу
            table_data = filtered_data[["Year", "Week", "SMN", "SMT", selected_index]]

            # Ініціалізація стану для сортування у session_state
            if "ascending_order" not in st.session_state:
                st.session_state["ascending_order"] = True
            if "descending_order" not in st.session_state:
                st.session_state["descending_order"] = False

            # Чекбокси для сортування
            def toggle_ascending():
                if st.session_state["ascending_order"]:
                    st.session_state["descending_order"] = False

            def toggle_descending():
                if st.session_state["descending_order"]:
                    st.session_state["ascending_order"] = False

            ascending_order = st.checkbox(
                "Сортувати за зростанням",
                value=st.session_state["ascending_order"],
                key="ascending_order",
                on_change=toggle_ascending
            )

            descending_order = st.checkbox(
                "Сортувати за спаданням",
                value=st.session_state["descending_order"],
                key="descending_order",
                on_change=toggle_descending
            )

            # Визначення порядку сортування
            order = ascending_order and not descending_order

            # Сортуємо дані за вибраним індексом
            sorted_table_data = table_data.sort_values(by=selected_index, ascending=order)

            # Відображення таблиці
            if sorted_table_data.empty:
                st.warning("Немає даних для відображення!")
            else:
                st.dataframe(sorted_table_data)

        with tab2:
            st.header("Графік")
            if filtered_data.empty:
                st.warning("Немає даних для відображення!")
            else:
                fig, ax = plt.subplots()
                ax.plot(filtered_data['Year'] + filtered_data['Week'] / 52, filtered_data[st.session_state.selected_index], color="purple")
                ax.set_title(f"{st.session_state.selected_index} для {st.session_state.selected_area}")
                ax.set_xlabel("Рік")
                ax.set_ylabel(st.session_state.selected_index)
                ax.grid(True)
                st.pyplot(fig)

        with tab3:
            st.header("Порівняння з іншими областями")
            comparison_data = data[
                (data['Year'].between(st.session_state.year_range[0], st.session_state.year_range[1])) &
                (data['Week'].between(st.session_state.week_range[0], st.session_state.week_range[1]))
                ]
            if comparison_data.empty:
                st.warning("Немає даних для порівняння!")
            else:
                # Розрахунок середніх значень для кожної області
                mean_values = comparison_data.groupby('area_name')[st.session_state.selected_index].mean().sort_values()

                fig, ax = plt.subplots(figsize=(10, 6))
                mean_values.plot(kind="bar", ax=ax, color="skyblue")
                ax.set_title(f"Середнє значення {st.session_state.selected_index} (всі області)")
                ax.set_ylabel(st.session_state.selected_index)
                ax.set_xlabel("Області")
                ax.axhline(
                    mean_values.loc[st.session_state.selected_area],
                    color="red", linestyle="--",
                    label=f"{st.session_state.selected_area}"
                )
                ax.legend()
                plt.xticks(rotation=45, ha='right')
                st.pyplot(fig)

if __name__ == "__main__":
    main()

# New changes