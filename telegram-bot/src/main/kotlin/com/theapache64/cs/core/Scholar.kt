package com.theapache64.cs.core

import com.theapache64.cs.models.rest.AddFeedbackRequest
import com.theapache64.cs.models.rest.CoronaAnswer
import com.theapache64.cs.models.rest.CoronaQuestion
import com.theapache64.cs.utils.GsonUtil
import com.theapache64.cs.utils.RestClient

object Scholar {

    private const val ANSWER_ENDPOINT = "https://covid-middleware.deepset.ai/api/bert/question"
    private const val FEEDBACK_ENDPOINT_FORMAT = "http://3.121.62.187/models/1/feedback"

    fun getAnswer(question: String): CoronaAnswer? {
        val jsonString = RestClient.post(
            ANSWER_ENDPOINT,
            null,
            CoronaQuestion(question)
        ).body!!.string()



        return GsonUtil.gson.fromJson(jsonString, CoronaAnswer::class.java)
    }

    fun addFeedback(documentId: Long, question: String, feedback: Char) {
        val feedbackString = getFeedbackString(feedback)
        val jsonString = RestClient.post(
            FEEDBACK_ENDPOINT_FORMAT,
            null,
            AddFeedbackRequest(feedbackString, question, documentId)
        ).body!!.string()
        println("Feedback response : $jsonString")
    }

    private fun getFeedbackString(feedback: Char): String {
        return when (feedback) {
            'r' -> "relevant"
            'f' -> "fake"
            'o' -> "outdated"
            'i' -> "irrelevant"
            else -> throw IllegalArgumentException("Undefined feedback char `$feedback`")
        }
    }
}