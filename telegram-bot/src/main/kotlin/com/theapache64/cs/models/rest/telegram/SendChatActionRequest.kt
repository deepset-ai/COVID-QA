package com.theapache64.cs.models.rest.telegram

import com.google.gson.annotations.SerializedName


data class SendChatActionRequest(
    @SerializedName("action")
    val action: String, // String
    @SerializedName("chat_id")
    val chatId: String // String
)