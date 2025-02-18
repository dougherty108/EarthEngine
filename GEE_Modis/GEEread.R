## MOD10A1.006 Terra Snow Cover Daily Global 500m
# https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD10A1#bands
setwd("~/Dropbox/currentprojects/MCM_MODIS")
      
# NDSI_Snow_Cover_Basic_QA
# # Bits 0-15: QA
# # 0: Best
# # 1: Good
# # 2: Ok
# # 3: Poor - not currently in use
# # 211: Night
# # 239: Ocean
# 
# NDSI_Snow_Cover_Class
# # 200		Missing data
# # 201		No decision
# # 211		Night
# # 237		Inland water
# # 239		Ocean
# # 250		Cloud
# Snow_Albedo_Daily_Tile_Class
# # 101		No decision
# # 111		Night
# # 125		Land
# # 137		Inland water
# # 139		Ocean
# # 150		Cloud

library(tidyverse)
library(lubridate)
library(MetBrewer)

# Read in data from GEE
readGEE <- function(filename) {
  txt = gsub("[][]", "", readLines(filename))
  txt = gsub("\"", "", txt)
  df = read.csv(text = txt, header = TRUE, skip = 1, quote="")
  return(df)
}

df0 = readGEE("Data/MODIS_multi0.csv")
df1 = readGEE("Data/MODIS_multi1.csv")
df2 = readGEE("Data/MODIS_multi2.csv")
df3 = readGEE("Data/MODIS_multi3.csv")
df4 = readGEE("Data/MODIS_multi4.csv")

df.albedo = df1 |> bind_rows(df2, df3, df4) |> 
  distinct() |> # delete duplicate rows
  mutate(ranking = dense_rank(desc(longitude))) |> # Convert longitude to lake name
  mutate(lake = case_when(ranking == 1 ~ 'LF',
                          ranking == 2 ~ 'LH',
                          ranking == 3 ~ 'ELB1',
                          ranking == 4 ~ 'ELB2',
                          ranking == 5 ~ 'WLB1',
                          ranking == 6 ~ 'WLB2')) |> 
  mutate(date = ymd(id)) |> 
  filter(as.numeric(NDSI_Snow_Cover_Basic_QA) %in% c(0:1)) |> # Filter good data
  filter(!Snow_Albedo_Daily_Tile_Class %in% c(101, 111, 150)) |> # Filter bad data
  mutate(year = if_else(month(date) > 7, year(date), year(date)-1)) |> 
  mutate(month = month(date)) |> 
  mutate(albedo = as.numeric(Snow_Albedo_Daily_Tile)) |> 
  mutate(lake = factor(lake, levels = c('WLB1','WLB2','ELB1','ELB2','LH','LF'))) |> 
  filter(!lake %in% c('WLB1','ELB1'))

sites = df.albedo |> group_by(lake, latitude, longitude) |> summarise()

ggplot(df.albedo |> filter(month >= 12 | month == 1)) +
  geom_boxplot(aes(x = as.character(year+1), y = albedo, fill = lake), 
               outlier.shape = NA, linewidth = 0.2,
               position=position_dodge(width = 0.5)) +
  labs(title = 'MODIS Albedo, Dec-Jan') +
  scale_fill_met_d(palette_name = 'Egypt') +
  theme_bw(base_size = 9) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1)) +
  theme(axis.title.x = element_blank())

ggsave('All_MODISalbedo_Dec-Jan.png', width = 5, height = 3, dpi = 500)

ggplot(df.albedo |> filter(month == 1)) +
  geom_boxplot(aes(x = as.character(year+1), y = albedo, fill = lake), 
               outlier.shape = NA, linewidth = 0.2,
               position=position_dodge(width = 0.5)) +
  labs(title = 'MODIS Albedo, Jan') +
  scale_fill_met_d(name = 'Egypt') +
  theme_bw(base_size = 9) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, vjust = 1)) +
  theme(axis.title.x = element_blank())

ggsave('All_MODISalbedo_Jan.png', width = 5, height = 3, dpi = 500)
