# Login
LOGIN_USERNAME = "//div[contains(@class, 'login-input')]//input[@type='text']"
LOGIN_PASSWORD = "//div[contains(@class, 'login-input')]//input[@type='password']"
LOGIN_BUTTON = "//button[contains(@class, 'login-button')]"

# Search modal
SEARCH_MODAL_DIV = "//div[@id='modal']/descendant::div[contains(@class, 'searchModal') and contains(@class, 'modalContainer')]"
CLOSE_SEARCH_MODAL_BUTTON = "//div[contains(@class, 'close')]" # respecto del modal
SEARCH_RESULT_CARD = "//a[contains(@class, 'searchResultItemWrapper')]" # hacer clic para seleccionar el evento, se puede uysar directamente con índices
SEARCH_RESULT_NAME = "//div[contains(@class, 'resultName')]"    # dentro de la tarjeta SEARCH_RESULT_CARD, ESTE NO SE PUEDE INDEXAR

# Favourites section
FAVOURITES_SECTION_TBODY = "//tbody[contains(@class, 'styles_favourite')]"
EVENT_ROW_TR = "//tr[contains(@class, 'eventRow')]" # RESPECTO DE FAVOURITES_SECTION
FAVOURITE_EVENT_ICON = "//td//div[contains(@class, 'disableHoverBackground')] //*[local-name()='svg' and contains(@class, 'favourite')]"   # respecto de EVENT_ROW_TR
# al hacer clic en favorito, dentro de la sección Favoritos, se elimina la fila del evento del dom

# SELECTIONS
# Market 1x2
EVENT_SELECTION_1X2_HOME_TD = "//td[@data-bet-group='wdw' and @data-outcome='h']"
EVENT_SELECTION_1X2_DRAW_TD = "//td[@data-bet-group='wdw' and @data-outcome='d']"
EVENT_SELECTION_1X2_AWAY_TD = "//td[@data-bet-group='wdw' and @data-outcome='a']"

# Market Asian Handicap
EVENT_SELECTION_AH_HOME_TD = "//td[@data-bet-group='ah' and @data-outcome='h']"
EVENT_SELECTION_AH_AWAY_TD = "//td[@data-bet-group='ah' and @data-outcome='a']"
# las selecciones contienen en su text() el valor de la cuota de la selección

# Placer modal
PLACER_MODAL_DIV = "//div[@id='placer']/div[contains(@class, 'draggable') and not(contains(@class, 'Blocker'))]"
CLOSE_PLACER_MODAL_DIV = "//div[contains(@class, 'Close')]"  # RESPECTO DE PLACER_MODAL_DIV


