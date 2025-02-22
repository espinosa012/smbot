import pandas as pd

class Pick:
    Date : str
    Event : str
    Participants : list = []
    Bet : dict = {} # {market, selection}
    MinOdds : float
    Stake : float   # cantidad a apostar en términos absolutos ??
    BetaminicStrategy : str
    MessageId : int

    def __init__(self, pick_dict : dict = None):
        self.Date = pick_dict["Date"] if pick_dict else ""
        self.Event = pick_dict["Event"] if pick_dict else ""
        self.Participants = pick_dict["Participants"] if pick_dict else []
        self.Bet = pick_dict["Bet"] if pick_dict else {"Market": "", "Selection": ""}
        self.MinOdds = pick_dict["MinOdds"] if pick_dict else 0
        self.Stake = pick_dict["Stake"] if pick_dict else 0
        self.BetaminicStrategy = pick_dict["BetaminicStrategy"] if pick_dict else ""
        self.UID = pick_dict["UID"] if pick_dict else -1

    def to_dict(self):
        return {
            "Date":self.Date,
            "Event":self.Event,
            "Participants":self.Participants,
            "Bet":self.Bet,
            "MinOdds":self.MinOdds,
            "Stake":self.Stake,
            "BetaminicStrategy":self.BetaminicStrategy,
            "UID":self.UID,
        }

    def to_dataframe(self):
        pick_dict : dict = self.to_dict()
        pick_dict["Participants"] = str.join(",", pick_dict["Participants"])
        pick_dict["Market"] = pick_dict["Bet"]["Market"]
        pick_dict["Selection"] = pick_dict["Bet"]["Selection"]
        del pick_dict["Bet"]
        del pick_dict["Stake"]
        return pd.Series(pick_dict)

    def save_to_csv(self):
        """
        Para almacenar en un fichero csv el pick
        """""
        # TODO: primero, comprobamos que no esté ya en el csv de histórico de picks
        history_pick_file_path : str = "data/pick.csv"  # TODO: guardar en config o lo que sea
        history_pick_df = pd.read_csv(history_pick_file_path, sep=';')

        filas_coincidentes = history_pick_df.loc[history_pick_df['UID'] == self.UID]
        if not history_pick_df.loc[history_pick_df['UID'] == self.UID].empty:
            # TODO: indicar en log que ya está en base de datos
            print("ya existe")
            return

        df = pd.concat([history_pick_df, self.to_dataframe()], ignore_index=True)
        df.to_csv(history_pick_file_path, index=False)

    def __str__(self):
        return str(self.to_dict())