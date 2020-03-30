package com.theapache64.cs.models

data class Feedback(
    val modelId:Int,
    val feedback: String,
    val question: String,
    val documentId: Long
)