package com.theapache64.cs.models.rest.telegram

import com.google.gson.annotations.SerializedName


data class AnswerCallbackRequest(
    @SerializedName("callback_query_id")
    val callbackQueryId: String // 123
)