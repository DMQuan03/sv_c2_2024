const USER = require("../module/user")


const User_Controller = {
    get_victims: async (req, res) => {
        try {
            const all_victims = await USER.find()
            return res.status(200).json({
                success: true,
                victims: all_victims
            })
        } catch (error) {
            return res.status(500).json({
                success: false,
                message: "error from server"
            })
        }
    },
}

module.exports = User_Controller