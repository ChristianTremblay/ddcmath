def kwh_and_cost(kw, cost=0.10):
    """
    Takes a pandas.DataFrame with a column named kW
    or a pandas.Series containing kW and gives back a dataFrame
    with 3 columns : kW | kWh | cost

    Total cost is just df['cost'].sum()
    """
    if isinstance(kw, pd.Series):
        df = pd.DataFrame(kw)
        df.columns = ["kW"]
    elif isinstance(kw, pd.DataFrame):
        df = kw
    else:
        raise ValueError("Provide pandas Series or DataFrame with a column named kW")

    kwh_cost = cost
    df["tvalue"] = df.index
    df["delta"] = (df["tvalue"] - df["tvalue"].shift()).fillna(0)
    df["prop"] = df["delta"] / pd.Timedelta("1h")
    df["kwh"] = df["kW"] * df["prop"]
    df["cost"] = df["kwh"] * kwh_cost
    return df[["kW", "kwh", "cost"]]
