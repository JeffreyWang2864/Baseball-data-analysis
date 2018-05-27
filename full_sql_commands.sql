-- Full SQL commands for the data analysis.
-- Display in order

-- ================================================================================

-- Get the max and the min year
SELECT MIN(yearID), MAX(yearID)
	FROM batting
	WHERE yearID != 0

-- Get the number of home runs each player have made in each year
SELECT yearID, HR
	FROM batting
	WHERE yearID != 0
	ORDER BY yearID

-- Get the summation of home runs have made in each year
SELECT yearID, SUM(HR)
	FROM batting
	WHERE yearID != 0
	GROUP BY yearID

-- Get the highest record in term of home run in 1880 and 2010
SELECT batting.playerID, yearID, teamID, MAX(HR), nameFirst, nameLast
	FROM batting
	INNER JOIN `master` ON batting.playerID=`master`.playerID
	WHERE yearID=1880 OR yearID=2010

-- Get the number of second base each player have made in each year
SELECT yearID, 2B
	FROM batting
	WHERE yearID != 0
	ORDER BY yearID

-- Get the summation of second base have made in each year
SELECT yearID, SUM(2B)
	FROM batting
	WHERE yearID != 0
	GROUP BY yearID

-- Get the number of third base each player have made in each year
SELECT yearID, 3B
	FROM batting
	WHERE yearID != 0
	ORDER BY yearID

-- Get the summation of third base have made in each year
SELECT yearID, SUM(3B)
	FROM batting
	WHERE yearID != 0
	GROUP BY yearID

-- Get the weight and year comparison
SELECT weight, birthYear
	FROM `master`

-- Get the weight-to-height ratio
SELECT weight, height
	FROM `master`

-- Get the average weight and height of all baseball player
SELECT AVG(weight), AVG(height)
	FROM `master`

-- Data analysis on whether things have an impact on salary
SELECT salaries.playerID, salaries.yearID, salaries.lgID, salaries.teamID, salary,
				G_all, GS, G_batting, G_defense, G_p, G_c, G_1b, G_2b, G_3b, G_ss, G_lf, G_cf,
				G_rf, G_of,
				weight, height, bats, throws, nameFirst, nameLast
	FROM salaries
	INNER JOIN appearances ON salaries.playerID = appearances.playerID and
													salaries.teamID = appearances.teamID and
													salaries.lgID = appearances.lgID and
													salaries.yearID = appearances.yearID
	INNER JOIN `master` ON salaries.playerID = `master`.playerID