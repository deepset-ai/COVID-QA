package com.theapache64.cs.models.rest.telegram

import com.google.gson.annotations.SerializedName


data class SendMessageResponse(
    @SerializedName("ok")
    val ok: Boolean, // true
    @SerializedName("result")
    val result: Result
) {
    data class Result(
        @SerializedName("chat")
        val chat: Chat,
        @SerializedName("date")
        val date: Long, // 1584216383
        @SerializedName("message_id")
        val messageId: Long, // 146
        @SerializedName("text")
        val text: String // This is some text
    ) {
        data class Chat(
            @SerializedName("id")
            val id: Long, // -1001423106120
            @SerializedName("title")
            val title: String, // Movie Monk
            @SerializedName("type")
            val type: String, // channel
            @SerializedName("username")
            val username: String // movie_m0nk
        )
    }
}