import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
df = pd.read_csv('air_quality_data.csv')

# Convertir la colonne timestamp en datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Distribution des niveaux de PM2.5 par ville
sns.boxplot(x='city', y='pm25', data=df)
plt.title('Distribution des niveaux de PM2.5 par ville')
plt.xlabel('Ville')
plt.ylabel('PM2.5')
plt.show()

# Série temporelle des niveaux de PM2.5 par ville
for city in df['city'].unique():
    df_city = df[df['city'] == city]
    df_city.set_index('timestamp', inplace=True)
    df_city['pm25'].plot(label=city)

plt.title('Niveaux de PM2.5 au fil du temps par ville')
plt.xlabel('Temps')
plt.ylabel('PM2.5')
plt.legend()
plt.show()

# Matrice de corrélation des polluants par ville
for city in df['city'].unique():
    df_city = df[df['city'] == city]
    corr = df_city[['pm25', 'pm10', 'no2', 'so2', 'o3', 'co']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title(f'Matrice de corrélation des polluants - {city}')
    plt.show()
