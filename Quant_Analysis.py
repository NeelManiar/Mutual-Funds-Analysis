
import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Mutual Fund Portfolio Comparison",
    page_icon="",
    layout="wide"
)

st.title("Mutual Funds Comparison")

st.write(
    "Upload two mutual fund portfolio statements to identify "
    "instruments that have been added, removed or retained."
)

st.divider()

uploaded_files = st.file_uploader(
    "Upload two portfolio files (CSV or Excel)",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

def load_file(file):

    file_extension = file.name.rsplit(".", 1)[-1].lower()

    file.seek(0)

    if file_extension == "csv":
        try:
            df = pd.read_csv(file, encoding="utf-8-sig")
        except UnicodeDecodeError:
            file.seek(0)
            df = pd.read_csv(file, encoding="latin-1")

    elif file_extension == "xlsx":
        df = pd.read_excel(file)

    else:
        raise ValueError("Unsupported file format.")

    df.columns = df.columns.astype(str).str.strip()

    if "NAME_OF_THE_INSTRUMENT" not in df.columns:
        raise ValueError(
            "Required column 'NAME_OF_THE_INSTRUMENT' is missing."
        )

    return df

def get_instruments(df):

    names = (
        df["NAME_OF_THE_INSTRUMENT"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    names = names[names != ""]
    instruments = {}

    for name in names:
        clean_name = " ".join(name.split())
        key = clean_name.casefold()

        if key not in instruments:
            instruments[key] = clean_name

    return instruments

if uploaded_files:

    if len(uploaded_files) != 2:
        st.warning("Please upload exactly two files for comparison.")

    else:

        file_data = {}
        errors = []

        # Load and validate both files
        for index, file in enumerate(uploaded_files):

            try:
                df = load_file(file)

                instruments = get_instruments(df)

                file_data[index] = {
                    "name": file.name,
                    "instruments": instruments
                }

                st.success(
                    f"{file.name} loaded successfully "
                    f"({len(instruments)} unique instruments)."
                )

            except Exception as e:
                errors.append(f"{file.name}: {str(e)}")

        if errors:
            for error in errors:
                st.error(error)

        elif len(file_data) == 2:

            st.divider()
            st.subheader("Select files to compare")

            file_options = {
                index: file_data[index]["name"]
                for index in file_data
            }

            col1, col2 = st.columns(2)

            with col1:
                baseline = st.selectbox(
                    "Earlier portfolio",
                    options=list(file_options.keys()),
                    format_func=lambda x: file_options[x],
                    index=0
                )

            with col2:
                comparison = st.selectbox(
                    "Later portfolio",
                    options=list(file_options.keys()),
                    format_func=lambda x: file_options[x],
                    index=1
                )

            if baseline == comparison:

                st.warning("Please select two different files.")

            else:

                old_data = file_data[baseline]["instruments"]
                new_data = file_data[comparison]["instruments"]

                # ------------------------------------------
                # SET COMPARISON
                # ------------------------------------------

                old_set = set(old_data.keys())
                new_set = set(new_data.keys())

                added = new_set - old_set
                removed = old_set - new_set
                unchanged = old_set & new_set

                added_names = sorted(
                    [new_data[key] for key in added],
                    key=str.casefold
                )

                removed_names = sorted(
                    [old_data[key] for key in removed],
                    key=str.casefold
                )

                unchanged_names = sorted(
                    [new_data[key] for key in unchanged],
                    key=str.casefold
                )

                # ------------------------------------------
                # SUMMARY
                # ------------------------------------------

                st.divider()
                st.subheader("Portfolio Comparison Results")

                st.caption(
                    f"Comparing {file_options[baseline]} "
                    f"against {file_options[comparison]}"
                )

                c1, c2, c3 = st.columns(3)

                c1.metric("Instruments Added", len(added_names))
                c2.metric("Instruments Removed", len(removed_names))
                c3.metric("Unchanged Instruments", len(unchanged_names))

                # ------------------------------------------
                # DISPLAY RESULTS
                # ------------------------------------------

                tab1, tab2, tab3 = st.tabs(
                    ["Added", "Removed", "Unchanged"]
                )

                with tab1:

                    st.subheader("Newly Added Instruments")

                    if added_names:
                        st.dataframe(
                            pd.DataFrame({"Instrument": added_names}),
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.success("No new instruments found.")

                with tab2:

                    st.subheader("Removed Instruments")

                    if removed_names:
                        st.dataframe(
                            pd.DataFrame({"Instrument": removed_names}),
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.success("No instruments were removed.")

                with tab3:

                    st.subheader("Retained Instruments")

                    if unchanged_names:
                        st.dataframe(
                            pd.DataFrame({"Instrument": unchanged_names}),
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.info("No unchanged instruments found.")

                # ------------------------------------------
                # DOWNLOAD REPORT
                # ------------------------------------------

                report = (
                    [{"Instrument": name, "Status": "Added"}
                     for name in added_names]
                    +
                    [{"Instrument": name, "Status": "Removed"}
                     for name in removed_names]
                    +
                    [{"Instrument": name, "Status": "Unchanged"}
                     for name in unchanged_names]
                )

                report_df = pd.DataFrame(report)

                st.divider()

                st.download_button(
                    label="Download Comparison Report",
                    data=report_df.to_csv(index=False).encode("utf-8-sig"),
                    file_name="portfolio_comparison.csv",
                    mime="text/csv"
                )

else:

    st.info("Upload two portfolio files to begin.")
