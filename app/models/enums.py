import enum


class ProfileActions(str, enum.Enum):
    """Actions to be performed on Pandas Profile"""

    SAMPLES = "samples"
    TABLES = "tables"
    ANALYSIS = "analysis"
    ALERTS = "alerts"
    DESCRIPTION = "description"
    CORRELATIONS = "correlations"
    MISSING = "missing"
    PACKAGE = "package"
    VARIABLE = "variable"
    DUPLICATES = "duplicates"
