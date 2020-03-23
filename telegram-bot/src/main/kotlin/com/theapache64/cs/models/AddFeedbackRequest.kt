package com.theapache64.cs.models

import com.google.gson.annotations.SerializedName


data class AddFeedbackRequest(
    @SerializedName("feedback")
    val feedback: String // relevant
)