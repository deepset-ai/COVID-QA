package com.theapache64.cs.utils

import com.theapache64.cs.models.Feedback

object FeedbackParser {
    private val feedbackRegEx = "(?<feedback>\\w)(?<documentId>\\d+)(?<question>.+)".toRegex()
    fun parse(data: String): Feedback {
        val match = feedbackRegEx.find(data)
        val groups = match!!.groups
        return Feedback(
            groups["feedback"]!!.value[0],
            groups["question"]!!.value,
            groups["documentId"]!!.value.toLong()
        )
    }
}