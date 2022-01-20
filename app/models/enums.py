import enum


class ProfileActions(str, enum.Enum):
    """Actions to be performed on Pandas Profile"""

    ANALYSIS = "analysis"
    TABLE = "table"
    VARIABLES = "variables"
    SCATTER = "scatter"
    CORRELATIONS = "correlations"
    MISSING = "missing"
    ALERTS = "alerts"
    PACKAGE = "package"
    SAMPLES = "samples"
    DUPLICATES = "duplicates"
    DESCRIPTION = "description"
