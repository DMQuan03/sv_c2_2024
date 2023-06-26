const Router2 = require("express").Router()
const ctrl = require("../controller/user")
Router2.get("/", ctrl.get_victims)
Router2.get("/location", ctrl.get_lat_lon)

module.exports = Router2

// CRUD : ==> create / read / update / delete