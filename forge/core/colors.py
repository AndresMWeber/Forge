import channels

color_lookup = {
    channels.DIRECTIONS.LEFT:
        {
            channels.LEVEL_PRIMARY: (1.0, 0.027, 0),
            channels.LEVEL_SECONDARY: (1.0, 0.027, 0),
            channels.LEVEL_TERTIARY: (1.0, 0.027, 0)
        },
    channels.DIRECTIONS.RIGHT:
        {
            channels.LEVEL_PRIMARY: (0.027, 0.027, 1.0),
            channels.LEVEL_SECONDARY: (0.027, 0.027, 1.0),
            channels.LEVEL_TERTIARY: (0.027, 0.027, 1.0)
        },
    channels.DIRECTIONS.CENTER:
        {
            channels.LEVEL_PRIMARY: (1.0, 0.551, 0.067),
            channels.LEVEL_SECONDARY: (1.0, 0.551, 0.067),
            channels.LEVEL_TERTIARY: (1.0, 0.551, 0.067)
        },
    channels.DIRECTIONS.NA:
        {
            channels.LEVEL_PRIMARY: (0.157, 0.314, 0.067),
            channels.LEVEL_SECONDARY: (0.157, 0.314, 0.067),
            channels.LEVEL_TERTIARY: (0.157, 0.314, 0.067)
        },
}
