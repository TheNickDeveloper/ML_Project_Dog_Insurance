library(dplyr)

# Clean the dataset
cleaned_data <- Dog_Bites_Data2018_expd_score %>%
# Remove records with empty or NA in Age column
filter(!is.na(Age) & Age != "") %>%

# Remove records with "Unknow" in Breed column (assuming typo - might want to also check for "Unknown")
filter(!grepl("^Unknow", Breed, ignore.case = TRUE)) %>%

# Remove records with "U" in Gender column
filter(Gender != "U")



converted_data <- cleaned_data %>%
  # Round up Age to integer (ceiling rounds up, round rounds to nearest)
  mutate(Age = ceiling(as.numeric(Age))) %>%
  
  # Convert SpayNeuter: False to 0, True to 1
  mutate(SpayNeuter = ifelse(SpayNeuter == "True", 1, 
                             ifelse(SpayNeuter == "False", 0, SpayNeuter))) %>%
  
  # Convert Borough to numeric codes
  mutate(Borough = case_when(
    Borough == "Manhattan" ~ 1,
    Borough == "Others" ~ 2,
    Borough == "Bronx" ~ 3,
    Borough == "Queens" ~ 4,
    Borough == "Staten Island" ~ 5,
    Borough == "Brooklyn" ~ 6,
    TRUE ~ NA_real_  # For any unexpected values
  )) %>%
  
  # Convert Gender: M to 1, F to 2
  mutate(Gender = case_when(
    Gender == "M" ~ 1,
    Gender == "F" ~ 2,
    TRUE ~ NA_real_  # For any unexpected values
  )) %>%
  
  # Convert Breed to numeric codes
  mutate(Breed = case_when(
    grepl("German Shepherd", Breed, ignore.case = TRUE) ~ 1,
    grepl("Pit Bull", Breed, ignore.case = TRUE) ~ 2,
    grepl("Rottweiler", Breed, ignore.case = TRUE) ~ 3,
    grepl("Bulldog", Breed, ignore.case = TRUE) ~ 4,
    grepl("Siberian Husky", Breed, ignore.case = TRUE) ~ 5,
    grepl("Mixed Breed", Breed, ignore.case = TRUE) ~ 6,
    TRUE ~ 7  # All other breeds
  )) %>%
  
  # Convert IsBite: False to 0, True to 1
  mutate(IsBite = ifelse(IsBite == "True", 1, 
                         ifelse(IsBite == "False", 0, IsBite)))



# Create the directory if it doesn't exist
dir.create("C:/Users/32355/Desktop/dog_data", showWarnings = FALSE, recursive = TRUE)

# Define the full file path
file_path <- "C:/Users/32355/Desktop/dog_data/transformed_dog_bites.csv"

# Export the cleaned data to CSV
write.csv(converted_data, file = file_path, row.names = FALSE)

# Verify the file was created
if(file.exists(file_path)) {
  message(paste("File successfully saved to:", file_path))
} else {
  warning("File was not created - please check the path permissions")
}

