const User = require("./user")
const Router = (app) => {
    app.use("/api/user", User)
}

module.exports = Router