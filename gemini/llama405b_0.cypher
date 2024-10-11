CREATE (vladimirPutin:PERSON {name: "Vladimir Putin"})
CREATE (russia:GPE {name: "Russia"})
CREATE (vladimirPutin)-[:IS_LEADER_OF]->(russia)

CREATE (ukraine:GPE {name: "Ukraine"})
CREATE (russia)-[:IS_IN_CONFLICT_WITH]->(ukraine)

CREATE (nato:ORG {name: "NATO"})
CREATE (russia)-[:IS_OPPOSED_TO]->(nato)

CREATE (usa:GPE {name: "USA"})
CREATE (russia)-[:IS_OPPOSED_TO]->(usa)

CREATE (europe:GPE {name: "Europe"})
CREATE (russia)-[:IS_OPPOSED_TO]->(europe)

CREATE (stPetersburg:LOC {name: "St Petersburg"})
CREATE (stPetersburg)-[:IS_IN]->(russia)

CREATE (moscow:LOC {name: "Moscow"})
CREATE (moscow)-[:IS_IN]->(russia)

CREATE (crimea:LOC {name: "Crimea"})
CREATE (crimea)-[:IS_IN]->(ukraine)
CREATE (crimea)-[:IS_ANNEXED_BY]->(russia)

CREATE (sergeiRyabkov:PERSON {name: "Sergei Ryabkov"})
CREATE (sergeiRyabkov)-[:IS_DEPUTY_FOREIGN_MINISTER_OF]->(russia)

CREATE (sirKeirStarmer:PERSON {name: "Sir Keir Starmer"})
CREATE (washington:LOC {name: "Washington"})
CREATE (sirKeirStarmer)-[:IS_IN]->(washington)

CREATE (joeBiden:PERSON {name: "Joe Biden"})
CREATE (joeBiden)-[:IS_PRESIDENT_OF]->(usa)

CREATE (uk:GPE {name: "UK"})
CREATE (uk)-[:IS_ALLY_OF]->(ukraine)

CREATE (hungary:GPE {name: "Hungary"})
CREATE (fide:ORG {name: "FIDE"})
CREATE (fide)-[:IS_BASED_IN]->(hungary)

CREATE (iran:GPE {name: "Iran"})
CREATE (iran)-[:IS_ALLY_OF]->(russia)

CREATE (kyiv:LOC {name: "Kyiv"})
CREATE (kyiv)-[:IS_IN]->(ukraine)

CREATE (vladimirPutin)-[:LOVES]->(russia)
CREATE (vladimirPutin)-[:HATES]->(nato)
CREATE (vladimirPutin)-[:HATES]->(usa)
CREATE (vladimirPutin)-[:HATES]->(europe)

CREATE (sirKeirStarmer)-[:LOVES]->(ukraine)
CREATE (sirKeirStarmer)-[:HATES]->(russia)

CREATE (joeBiden)-[:LOVES]->(ukraine)
CREATE (joeBiden)-[:HATES]->(russia)

CREATE (iran)-[:LOVES]->(russia)
CREATE (iran)-[:HATES]->(ukraine)

CREATE (uk)-[:LOVES]->(ukraine)
CREATE (uk)-[:HATES]->(russia)

CREATE (hungary)-[:MEHS]->(fide)
CREATE (fide)-[:MEHS]->(russia)

CREATE (vladimirPutin)-[:IS_OPPOSED_TO]->(ukraine) 
CREATE (vladimirPutin)-[:IS_OPPOSED_TO]->(nato) 
CREATE (vladimirPutin)-[:IS_OPPOSED_TO]->(usa) 
CREATE (vladimirPutin)-[:IS_OPPOSED_TO]->(europe) 

CREATE (vladimirPutin)-[:IS_LEADER_OF]->(russia {start_date: "2000-01-01"})