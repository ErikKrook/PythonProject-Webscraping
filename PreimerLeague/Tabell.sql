/*
Börja med att tvätta datat med hjälp av följande kod snutt som tar bort frågetecken runt resultat raden
--UPDATE Resultat
--SET Resultat = SUBSTRING(Resultat, 2, LEN(Resultat) -2)
*/

 -- Skapar en CTE som lägger till nya kolumner Utfall_Hemma, Utfall_Borta, H_Mål och B_Mål till Resultat-tabellen
WITH cte AS (
SELECT *, 
	CASE WHEN LEFT(Resultat, 1) > RIGHT(Resultat, 1) THEN 'W'
		WHEN LEFT(Resultat, 1) < RIGHT(Resultat, 1) THEN 'L'
		ELSE 'D' END AS Utfall_Hemma,
		CASE WHEN LEFT(Resultat, 1) < RIGHT(Resultat, 1) THEN 'W'
		WHEN LEFT(Resultat, 1) > RIGHT(Resultat, 1) THEN 'L'
		ELSE 'D' END AS Utfall_Borta,
		CAST( LEFT(Resultat, 1) AS smallint) H_Mål,
		CAST( RIGHT(Resultat, 1) AS smallint) B_Mål
FROM Resultat ) 


SELECT Hemma [Lag], --Summerar datat och skriver ut tabellen
		Vinst + Oavjort + Förlust AS Matcher, 
		Vinst, 
		Oavjort, 
		Förlust, 
		Gjorda AS GM, 
		Insläppta AS IM, 
		Gjorda - Insläppta AS MS, 
		Vinst*3 + Oavjort AS Poäng 
FROM ( SELECT Hemma, -- Aggregerar data för hemma och bortatabellen
		SUM(h.W_count + b.W_count) AS Vinst, 
		SUM(h.D_count + b.D_count) AS Oavjort, 
		SUM(h.L_count + b.L_count) AS Förlust,
		SUM(h.Gjorda + b.Gjorda) AS Gjorda, 
		SUM(h.Insläppta + b.Insläppta) AS Insläppta
		FROM (SELECT Hemma, -- Aggregerar data per hemmalag
					--Räknar ut hur många vinst, lika samt flrluster varje lag har
					   COUNT(CASE WHEN Utfall_Hemma = 'W' THEN 1 ELSE NULL END) AS W_count, 
					   COUNT(CASE WHEN Utfall_Hemma = 'D' THEN 1 ELSE NULL END) AS D_count, 
					   COUNT(CASE WHEN Utfall_Hemma = 'L' THEN 1 ELSE NULL END) AS L_count,
					   -- Summerar målstatistiken
					   SUM(H_Mål) AS Gjorda,
					   SUM(B_Mål) AS Insläppta
				FROM cte 
				GROUP BY Hemma) h
		INNER JOIN  (SELECT Borta, -- Aggregerar data per bortalag
							   COUNT(CASE WHEN Utfall_Borta = 'W' THEN 1 ELSE NULL END) AS W_count,
							   COUNT(CASE WHEN Utfall_Borta = 'D' THEN 1 ELSE NULL END) AS D_count, 
							   COUNT(CASE WHEN Utfall_Borta = 'L' THEN 1 ELSE NULL END) AS L_count,
							   SUM(B_Mål) AS Gjorda,
							   SUM(H_Mål) AS Insläppta
						FROM cte 
						GROUP BY Borta ) b
		ON h.Hemma = b.Borta
		GROUP BY Hemma ) sub
ORDER BY --Soretera tabellen i rätt ordning
	Poäng DESC, 
	MS DESC, 
	GM DESC, 
	[Lag]
