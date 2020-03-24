package com.theapache64.cs.core

import com.theapache64.cs.models.CoronaAnswer
import com.theapache64.cs.models.CoronaQuestion
import com.theapache64.cs.utils.GsonUtil
import com.theapache64.cs.utils.RestClient

object Scholar {

    private const val API_ENDPOINT = "https://covid-middleware.deepset.ai/api/bert/question"

    fun getAnswer(question: String): CoronaAnswer? {
        val jsonString = RestClient.post(
            API_ENDPOINT,
            null,
            CoronaQuestion(question)
        ).body!!.string()

        return GsonUtil.gson.fromJson(jsonString, CoronaAnswer::class.java)
    }
}