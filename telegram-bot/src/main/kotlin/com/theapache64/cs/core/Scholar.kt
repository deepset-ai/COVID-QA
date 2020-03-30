package com.theapache64.cs.core

import com.theapache64.cs.models.Feedback
import com.theapache64.cs.models.rest.AddFeedbackRequest
import com.theapache64.cs.models.rest.CoronaAnswer
import com.theapache64.cs.models.rest.CoronaQuestion
import com.theapache64.cs.utils.GsonUtil
import com.theapache64.cs.utils.RestClient

object Scholar {

    private const val BASE_URL = "https://covid-backend.deepset.ai"

    fun getAnswer(question: String): CoronaAnswer? {
        val jsonString = RestClient.post(
            "$BASE_URL/question/ask",
            null,
            CoronaQuestion(
                arrayOf(question)
            )
        ).body!!.string()

        println(jsonString)

        return GsonUtil.gson.fromJson(jsonString, CoronaAnswer::class.java)
    }

    fun addFeedback(feedback: Feedback) {
        val jsonString = RestClient.post(
            "$BASE_URL/models/${feedback.modelId}/feedback",
            null,
            AddFeedbackRequest(
                feedback.feedback,
                feedback.question,
                feedback.documentId
            )
        ).body!!.string()
        println("Feedback response : $jsonString")
    }


}