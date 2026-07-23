"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel
import glob
import os
import pandas as pd


def clean_campaign_data():
    input_files = glob.glob("files/input/*.csv.zip")
    df_list = [pd.read_csv(file, compression="zip") for file in input_files]
    df = pd.concat(df_list, ignore_index=True)

    os.makedirs("files/output", exist_ok=True)

  
    client_df = pd.DataFrame()
    client_df["client_id"] = df["client_id"]
    client_df["age"] = df["age"]
    client_df["job"] = (
        df["job"].astype(str).str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    )
    client_df["marital"] = df["marital"]
    client_df["education"] = (
        df["education"].astype(str).str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    )
    client_df["credit_default"] = (df["credit_default"] == "yes").astype(int)
    mortgage_col = "mortgage" if "mortgage" in df.columns else "mortage"
    client_df["mortgage"] = (df[mortgage_col] == "yes").astype(int)

    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }

    campaign_df = pd.DataFrame()
    campaign_df["client_id"] = df["client_id"]
    campaign_df["number_contacts"] = df["number_contacts"]
    campaign_df["contact_duration"] = df["contact_duration"]
    
    prev_col = "previous_campaign_contacts" if "previous_campaign_contacts" in df.columns else "previous_campaing_contacts"
    campaign_df["previous_campaign_contacts"] = df[prev_col]
    
    campaign_df["previous_outcome"] = (df["previous_outcome"] == "success").astype(int)
    campaign_df["campaign_outcome"] = (df["campaign_outcome"] == "yes").astype(int)

    month_str = df["month"].astype(str).str.lower().map(month_map).fillna(df["month"].astype(str).str.zfill(2))
    day_str = df["day"].astype(str).str.zfill(2)
    campaign_df["last_contact_date"] = "2022-" + month_str + "-" + day_str

   
    cons_price_col = "cons_price_idx" if "cons_price_idx" in df.columns else "const_price_idx"
    euribor_col = "euribor_three_months" if "euribor_three_months" in df.columns else "eurobor_three_months"

    economics_df = pd.DataFrame()
    economics_df["client_id"] = df["client_id"]
    economics_df["cons_price_idx"] = df[cons_price_col]
    economics_df["euribor_three_months"] = df[euribor_col]

   
    client_df.to_csv("files/output/client.csv", index=False)
    campaign_df.to_csv("files/output/campaign.csv", index=False)
    economics_df.to_csv("files/output/economics.csv", index=False)


if __name__ == "__main__":
    clean_campaign_data()