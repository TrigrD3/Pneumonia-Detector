package com.example.pneumoniadetector.ui.history

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.paging.*
import com.example.pneumoniadetector.data.adapter.ResultPagingSource
import com.example.pneumoniadetector.data.remote.response.ResultItem
import com.example.pneumoniadetector.data.remote.retrofit.ApiConfig

class HistoryViewModel : ViewModel() {

    private val _text = MutableLiveData<String>().apply {
        value = ""
    }
    val text: LiveData<String> = _text

    private val webApiService = ApiConfig.getApiService()

    fun resultsData(): LiveData<PagingData<ResultItem>>{
        return Pager(
            config = PagingConfig(
                pageSize = 5,
                initialLoadSize = 5
            ),
            pagingSourceFactory = {
                ResultPagingSource(webApiService)
            }
        ).liveData
    }

    val data:LiveData<PagingData<ResultItem>> = resultsData().cachedIn(viewModelScope)
}