from shiny import App, ui, render
import palmerpenguins
import pandas as pd
import seaborn as sns

# Load the Palmer Penguins dataset
penguins_data = palmerpenguins.load_penguins()

# Define the user interface of the app
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        # Sidebar layout for filters
        ui.panel_sidebar(
            "Penguin Data Filters",
            ui.input_slider("body_mass", "Penguin Body Mass (grams)", min=2000, max=7000, value=4000),
            ui.input_checkbox_group(
                "chosen_species",
                "Choose Species",
                choices=["Adelie", "Gentoo", "Chinstrap"],
                selected=["Adelie", "Gentoo"]
            ),
            ui.input_checkbox_group(
                "chosen_island",
                "Select Island",
                choices=["Biscoe", "Dream", "Torgersen"],
                selected=["Dream", "Torgersen"]
            ),
            ui.hr(),  # Correct use of horizontal rule
            ui.a("View Source on GitHub", href="https://github.com/your-username/your-repository"),
            ui.a("Explore the App", href="https://github.com/your-username/your-repository/app.py"),
        ),
        # Main panel for displaying outputs
        ui.panel_main(
            ui.output_text("total_count"),
            ui.output_plot("plot_bill_metrics"),
            ui.output_table("display_data")
        )
    )
)

# Define server logic to handle user inputs and render outputs
def server(input, output, session):
    @output
    @render.text
    def total_count():
        df = apply_filters(input)
        return f"{df.shape[0]} penguins"

    @output
    @render.plot(alt="Bill length vs. depth scatterplot")
    def plot_bill_metrics():
        df = apply_filters(input)
        sns.set(style="whitegrid")
        ax = sns.scatterplot(
            data=df,
            x="bill_length_mm",
            y="bill_depth_mm",
            hue="species",
            palette="viridis",
            style="island"
        )
        ax.set(title="Bill Length vs Depth by Species")
        return ax.figure

    @output
    @render.table
    def display_data():
        df = apply_filters(input)
        return df[["species", "island", "bill_length_mm", "bill_depth_mm", "body_mass_g"]]

    def apply_filters(input):
        df = penguins_data
        if input.chosen_species():
            df = df[df["species"].isin(input.chosen_species())]
        if input.chosen_island():
            df = df[df["island"].isin(input.chosen_island())]
        df = df[df["body_mass_g"] <= input.body_mass()]
        return df

# Create the app
app = App(app_ui, server)

# Run the app
if __name__ == "__main__":
    app.run(port=9999, host="0.0.0.0")
