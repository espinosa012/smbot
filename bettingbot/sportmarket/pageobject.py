# Login
LOGIN_USERNAME = "//input[@data-testid='username']"
LOGIN_PASSWORD = "//input[@data-testid='password']"
LOGIN_BUTTON = "//button[@data-testid='submit']"

# Announce modal
ANNOUNCE_MODAL = "//div[contains(@class, 'announcementContentContainer')]/ancestor::div[contains(@class, 'modalBody')]"
CLOSE_ANNOUNCE_MODAL_BUTTON = "//button[contains(@class, 'styles_button')]" # respecto del modal ANNOUNCE_MODAL

# Home
SEARCH_BUTTON = "//li[contains(@class, 'navSearchItem')]//*[local-name()='svg']/ancestor::div[1]"

# Search modal
SEARCH_MODAL_DIV = "//div[@id='modal']/descendant::div[contains(@class, 'searchModal') and contains(@class, 'modalContainer')]"
SEARCH_BAR_INPUT = "//div[contains(@class, 'search')]//input[contains(@class, 'search')]"
CLOSE_SEARCH_MODAL_BUTTON = "//div[contains(@class, 'close')]" # respecto del modal
SEARCH_RESULT_CARD = "//a[contains(@class, 'searchResultItemWrapper')]" # hacer clic para seleccionar el evento, se puede uysar directamente con índices
SEARCH_RESULT_NAME = "//div[contains(@class, 'resultName')]"    # dentro de la tarjeta SEARCH_RESULT_CARD, ESTE NO SE PUEDE INDEXAR

# Favourites section
FAVOURITES_SECTION_TBODY = "//tbody[contains(@class, 'styles_favourite')]" # se puede usar para comprobar que hemos hecho login bien
EVENT_ROW_TR = "//tr[contains(@class, 'eventRow')]" # RESPECTO DE FAVOURITES_SECTION
FAVOURITE_EVENT_ICON = "//*[local-name()='svg' and contains(@class, 'favouriteIcon')]"
# al hacer clic en favorito, dentro de la sección Favoritos, se elimina la fila del evento del dom

# SELECTIONS
# Market 1x2
EVENT_SELECTION_1X2_HOME_TD = "//td[@data-bet-group='wdw' and @data-outcome='h']"
EVENT_SELECTION_1X2_DRAW_TD = "//td[@data-bet-group='wdw' and @data-outcome='d']"
EVENT_SELECTION_1X2_AWAY_TD = "//td[@data-bet-group='wdw' and @data-outcome='a']"

# Market Total Goals
EVENT_SELECTION_TOTAL_GOALS_OVER_TD = "//td[@data-bet-group='ahou' and @data-outcome='over']"
EVENT_SELECTION_TOTAL_GOALS_UNDER_TD = "//td[@data-bet-group='ahou' and @data-outcome='under']"

# Market Asian Handicap
EVENT_SELECTION_AH_HOME_TD = "//td[@data-bet-group='ah' and @data-outcome='h']"
EVENT_SELECTION_AH_AWAY_TD = "//td[@data-bet-group='ah' and @data-outcome='a']"

# Placer modal
PLACER_MODAL_DIV = "//div[@id='placer']/div[contains(@class, 'draggable') and not(contains(@class, 'Blocker'))]"
CLOSE_PLACER_MODAL_DIV = "//div[contains(@class, 'Close')]"  # RESPECTO DE PLACER_MODAL_DIV
STAKE_INPUT = "//input[contains(@class, 'stake-input')]"
PLACE_BET_BUTTON = "//button[contains(@class, 'placeButton')]"
BEST_ODDS_SPAN = "//div[contains(@class, 'styles_egg')]/descendant::div[contains(@class, 'styles_chiclet') and not(contains(@class, 'classic'))][1]/descendant::span[contains(@class, '_price_')]"
BEST_ODDS_MAX_STAKE_SPAN = "//div[contains(@class, 'styles_egg')]/descendant::div[contains(@class, 'styles_chiclet') and not(contains(@class, 'classic'))][1]/descendant::span[contains(@class, '_stake_')]"
BOOKIE_PRICE_ROW = "//div[contains(@class, 'bookieAccountPrices')]"

# Place confirmation modal
PLACE_CONFIRMATION_MODAL_DIV = "//div[contains(@class, 'placeConfirmationModal')]"
PLACE_CONFIRMATION_MODAL_FOOTER_DIV = "//div[contains(@class, 'placeConfirmationModalFooter')]"
CONFIRM_PLACE_BUTTON = "//button[contains(@class, 'button')][2]"