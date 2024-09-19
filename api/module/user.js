const mongoose = require('mongoose'); // Erase if already required

// Declare the Schema of the Mongo model
var userSchema = new mongoose.Schema({
    user_name: {
        type: String,
        default: "user_default"
    },
    ip_address: {
        type: String,
        default: "0.0.0.0"
    },
    system: {
        type: String,
        default: "Windows"
    },
    release: {
        type: String,
        default: "empty"
    },
    version: {
        type: String,
        default: "empty"
    },
    machine: {
        type: String,
        default: "empty"
    },
    online: {
        type: Boolean,
        default: false
    },
    session: {
        type: Number,
        default: 0
    },
    ip_socket: {
        type: String,
        default: "null"
    }
});

//Export the model
module.exports = mongoose.model('User', userSchema);