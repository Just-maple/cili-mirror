<template>
  <div style="padding: 10px">
    <div>
      <el-input style="width: 100% " placeholder="你要冲啥？" @keyup.enter.native="getData(1)"  v-model="key"></el-input>
      <el-button style="width: 100%;margin-top: 10px" @click="getData(1)">冲</el-button>
    </div>
    <div v-if="isLoading" style="margin-top: 10px;font-size: 100%">
      <i class="el-icon-loading"></i> 在冲
    </div>
    <div style="margin-top: 10px">
      <el-radio-group v-model="order" @change="getData(current_page)">
        <el-radio  :label="1">收录日期</el-radio>
        <el-radio :label="2">大小</el-radio>
        <el-radio  :label="3">文件数</el-radio>
    </el-radio-group>
    </div>
    <div style="clear: both;margin-top: 10px" v-if="data">
      <el-pagination
        small
        style="width: 100%"
        @current-change="getData"
        layout="prev, pager, next"
        :current-page="current_page"
        :page-size="data.magnets.length"
        :page-count="Math.min(parseInt(data.total/data.magnets.length),100)">
      </el-pagination>
      共 {{data.total}} 个结果
      <div v-for="cili in data.magnets" style="margin-top: 10px;text-align: left">
        <el-card shadow="hover">
          <div style="font-size: 120%" v-html="cili.title"></div>
          <div>文件数：{{cili.files_cnt}}</div>
          <div>大小：{{cili.size}}</div>
          <div>创建时间：{{cili.t_create}}</div>
          <div>
            磁力链接：
            <a style="word-wrap:break-word;" :href="`magnet:?xt=urn:btih:${cili.magnet}`">magnet:?xt=urn:btih:{{cili.magnet}}</a>
          </div>
        </el-card>
      </div>

      <div v-if="isLoading" style="margin-top: 10px;font-size: 100%">
        <i class="el-icon-loading"></i> 在冲
      </div>
      <el-pagination
        small
        style="width: 100%"
        @current-change="getData"
        layout="prev, pager, next"
        :current-page="current_page"
        :page-size="data.magnets.length"
        :page-count="Math.min(parseInt(data.total/data.magnets.length),100)">
      </el-pagination>
    </div>
  </div>
</template>

<script>
  export default {
    name: "index",
    data() {
      return {
        key: "",
        data: "",
        order: 1,
        isLoading:false,
        current_page:1
      }
    },
    created() {
    },
    methods: {
      getData(page) {
        if(!this.key || this.isLoading ){
          return
        }
        this.isLoading = true
        this.current_page = page
        this.httpGet(`/api/key?key=${this.key}&page=${page}&order=${this.order}`, res => {
          this.data = res.data.data
          this.isLoading = false
        }, e => {
          console.log(e)
          this.data = ''
          this.isLoading = false
          alert("萎了冲不了，请稍后再试")
        })
      }
    }
  }
</script>

<style scoped>

</style>
