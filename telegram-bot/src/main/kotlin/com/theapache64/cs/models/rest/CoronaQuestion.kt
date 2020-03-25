package com.theapache64.cs.models.rest

import com.google.gson.annotations.SerializedName

class CoronaQuestion(
    @SerializedName("questions")
    val questions: Array<String>, // How does corona spread?
    @SerializedName("top_k_retriever")
    val resultCount: Int = 1
)