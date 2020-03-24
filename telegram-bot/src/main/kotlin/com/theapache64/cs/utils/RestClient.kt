package com.theapache64.cs.utils

import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import java.util.concurrent.TimeUnit

object RestClient {

    fun get(url: String, headers: Map<String, String>? = null): Response {
        return call("GET", url, headers, null)
    }

    private fun getNewOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .followRedirects(true)
            .followSslRedirects(true)
            .build()
    }

    private fun call(method: String, url: String, headers: Map<String, String>?, body: Any?): Response {


        val request = Request.Builder()
            .url(url)

        if (body != null) {
            val json = GsonUtil.gson.toJson(body)

            println("$method : $url -> $json")

            request.addHeader("Content-Type", "application/json")
            request.method(method, json.toRequestBody())
        } else {
            request.method(method, null)
        }

        if (headers != null) {
            for (header in headers) {
                request.addHeader(header.key, header.value)
            }
        }

        request.addHeader(
            "User-Agent",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        )

        return getNewOkHttpClient().newCall(request.build()).execute()
    }

    fun post(url: String, headers: Map<String, String>?, body: Any): Response {
        return call(
            "POST",
            url,
            headers,
            body
        )
    }

    fun put(
        url: String,
        headers: Map<String, String>,
        body: Any
    ): Response {
        return call(
            "PUT",
            url,
            headers,
            body
        )
    }
}