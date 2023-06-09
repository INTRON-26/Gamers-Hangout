const express = require('express');
const mongoose = require('mongoose')
const cors = require('cors')
require('dotenv').config();

const app = express();

app.use(express.json())
app.use(cors());

// User Routes
const userRouter = require('./routes/UserRoute');
app.use('/api/users',userRouter);

mongoose.connect("mongodb+srv://admin:intron%40135@cluster0.cyn8jcn.mongodb.net/?retryWrites=true&w=majority", {useNewUrlParser: true}
).then(() => {
    console.log('Connected to MongoDB')
}).catch((err) => {
    console.log(err);
})

const port = process.env.PORT || 3000;
app.listen(port,() => {
    console.log('Server listening on port 3000')
})