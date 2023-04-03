import collect as c
from mysql import data_save


df = c.library_location()
data_save(df, 'library_location')

df = c.gu_libraries()
data_save(df, 'gu_libraries')

df = c.gu_materials_per()
data_save(df, 'gu_materials_per')

df = c.gu_population_per()
data_save(df, 'gu_population_per')

df = c.gu_librarybudget()
data_save(df, 'gu_librarybudget')

df = c.library_users()
data_save(df, 'library_users')

df = c.library_rent()
data_save(df, 'library_rent')

df = c.gu_youth_population()
data_save(df, 'gu_youth_population')

df = c.gu_averageincome()
data_save(df, 'gu_averageincome')

df = c.gu_satisfaction()
data_save(df, 'gu_satisfaction')

df = c.gu_disadv_budget()
data_save(df, 'gu_disadv_budget')

df = c.gu_disadv_users()
data_save(df, 'gu_disadv_users')

df = c.gu_ages()
data_save(df, 'gu_ages')

df = c.gu_schoolage()
data_save(df, 'gu_schoolage')
