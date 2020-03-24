package com.theapache64.cs.models

import com.google.gson.annotations.SerializedName

data class CoronaQuestion(
    @SerializedName("question")
    val question: String // How does corona spread?
)