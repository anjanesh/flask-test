ProductMovement = """
SELECT pm.`from_location`, pm.`to_location`, pm.`product_id`, pm.`qty`,
(SELECT `name` FROM Product p WHERE p.`product_id` = pm.`product_id`) AS `product_name`
FROM `ProductMovement` pm
WHERE
pm.`from_location` = %s OR
pm.`to_location` = %s
"""

ProductMovement_to_Location = """
SELECT pm.`from_location`, pm.`to_location`, pm.`qty`
FROM `ProductMovement` pm
WHERE pm.`product_id` = %s AND pm.`to_location` = %s
"""

ProductMovement_add = """
INSERT INTO `ProductMovement` SET
`timestamp` = NOW(),
`from_location` = %s,
`to_location` = %s,
`product_id` = %s,
`qty` = %s
"""

location_add = "INSERT INTO `Location` (`location_id`, `name`) VALUES (NULL, %s);"
location_edit = "UPDATE `Location` SET `name` = '%s' WHERE `location_id` = %s;"

move_list = """
SELECT
pm.movement_id, pm.timestamp, pm.qty,
(SELECT name FROM Product p where pm.product_id = p.product_id) as name,
(SELECT name FROM Location l where pm.from_location = l.location_id) as from_location,
(SELECT name FROM Location l where pm.to_location = l.location_id) as to_location
FROM `ProductMovement` pm
"""

move_push = """
INSERT INTO `ProductMovement` SET
`timestamp` = NOW(),
`from_location` = 0,
`to_location` = %s,
`product_id` = %s,
`qty` = %s
"""

data_movement = """
SELECT pm.`from_location`, pm.`to_location`, pm.`qty`,
(SELECT `name` FROM Location l WHERE l.`location_id` = pm.`from_location`) AS `from_location_name`,
(SELECT `name` FROM Location l WHERE l.`location_id` = pm.`to_location`) AS `to_location_name`
FROM `ProductMovement` pm
WHERE pm.`product_id` = %s
"""