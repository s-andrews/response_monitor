library(shiny)
library(bslib)

# Define UI for application that draws a histogram

readr::read_tsv("../../cron/site_list.txt",col_names = "site") |>
  dplyr::pull(site) -> sites

ui <- page_sidebar(
  
  title=div(
    "Website Response Monitor",
     class="text-center fs-2 bg-dark text-light",
    style="width:100%"
  ),
  
  sidebar = sidebar(
    width = "30%",

    selectInput(
      inputId = "url_choice",
      label="Pick a website",
      choices = sites
    ),
    
    radioButtons(
      inputId = "duration",
      label="Over How Long",
      choices = c("A day","A week","A month")
    ),
    
    dateInput(
      inputId = "date",
      label = "To Which Date",
      value=Sys.Date()
    )
    
  ),
  
  plotOutput(outputId="response_plot")
    
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    output$response_plot <- renderPlot({
      
      get_data() |>
        ggplot2::ggplot(ggplot2::aes(x=Time,y=Response/1000,colour=Code)) +
        ggplot2::geom_point() +
        ggplot2::theme_bw(base_size=20) +
        ggplot2::scale_colour_manual(values=c(`200` = "green3", FAIL="red2", `404`="blue2", `500`="red2")) +
        ggplot2::ggtitle(get_title()) +
        ggplot2::ylab("Reponse time (seconds)") +
        ggplot2::facet_grid(cols=ggplot2::vars(Date)) +
        ggplot2::theme(panel.spacing.x = ggplot2::unit(0,"lines")) +
        ggplot2::coord_cartesian(ylim=c(0,30))
      
    })
    
    
    get_title <- reactive({
      input$url_choice
    })
    
    
    get_data <- reactive({
      
      if (input$duration == "A day") {
        return(load_data() |> dplyr::filter(Date==input$date))
      }
      
      if (input$duration == "A week") {
        return(load_data() |> dplyr::filter(Date<=input$date, Date>=input$date-7))
      }
      
      if (input$duration == "A month") {
        return(load_data() |> dplyr::filter(Date<=input$date, Date>=input$date-30))
      }
      
            
    })
    
    
    load_data <- reactive({
      stringr::str_replace_all(input$url_choice,"/","_") -> file_name
      readr::read_delim(
        paste0("../../data/",file_name), 
        col_names=c("Date","Time","Code","Response"),
        col_types="??cn"
      ) |>
        dplyr::mutate(Response=replace(Response,Response>30000,30000))
    })
    
}

# Run the application 
shinyApp(ui = ui, server = server)
