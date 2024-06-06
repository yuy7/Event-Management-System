<template>
<navbar></navbar>
  <div class='cal'>
    <div class='cal-left'>
      <div class='cal-left-title'>
        <h2>欢迎来到活动管理系统！</h2>
      </div>
      <div class='cal-left-label'>
        <label>
          <input
            type='checkbox'
            :checked='calendarOptions.weekends'
            @change='handleWeekendsToggle'
          />
          是否显示周末
        </label>
      </div>
      <div class='cal-left-title'>
        <h2>所有活动安排({{ currentEvents.length }})</h2>
        <ul>
          <li v-for='event in currentEvents' :key='event.id'>
            <h3>{{ event.startStr }}</h3>
            {{ event.title }}
          </li>
        </ul>
      </div>
    </div>
    <div class='cal-main'>
      <FullCalendar
        class='cal-calendar'
        :options='calendarOptions'
      >
        <template v-slot:eventContent='arg'>
          <b>{{ arg.timeText }}</b>
          {{ arg.event.title }}
        </template>
      </FullCalendar>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { INITIAL_EVENTS, createEventId } from './event-utils'
import Navbar from './navbar.vue';
import axios from 'axios';

export default defineComponent({
  components: {
    FullCalendar,
	Navbar,
  },
  data() {
    return {
      calendarOptions: {
		// 引入的插件
        plugins: [
          dayGridPlugin,
          timeGridPlugin,
          interactionPlugin
        ],
		// 日历头部按钮位置
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
		// 日历头部按钮中文转换
		buttonText: {
			today: '今天',
			month: '月',
			week: '周',
			day: '天'
		},
		aspectRatio: '1.5', // 设置日历单元格宽高比
		allDaySlot: false, // 周、日视图时，all-day不显示
		displayEventTime: false, // 是否显示事件时间
		dayMaxEvents: true,
		eventColor: '#2c3e50', // 全部日历日程背景色
		eventLimit: true, // 设置月日程，与all-day slot 的最大显示数量，超过的通过弹窗展示
		eventTimeFormat: {
			hour: 'numeric',
			minute: '2-digit',
			hour12: false
		},
		events: this.fetchEvents, // 日程数组
		editable: false, // 是否可以进行（拖动、缩放）修改
		eventStartEditable: false, // Event日程开始时间可以改变，默认为true，若为false,则表示开始结束时间范围不能拉伸，只能拖拽
		eventDurationEditable: false, // Event日程的开始结束时间距离是否可以改变，默认为true,若为false，则表示开始结束时间范围不能拉伸，只能拖拽
		firstDay: '1', // 设置一周中显示的第一天是周几，周日是0，周一是1，以此类推
		initialView: 'dayGridMonth', // 指定默认显示视图
		//initialEvents:INITIAL_EVENTS, // 默认事件
		locale: 'zh-ch', // 切换语言，当前为中文
		navLinks: true, // 天链接
		slotLabelFormat: {
			hour: '2-digit',
			minute: '2-digit',
			meridiem: false,
			hour12: false // 设置时间为24小时制
		},
		selectable: true, // 是否可以选中日历格
		selectMirror: true,
		selectMinDistance: 0, // 选中日历格的最小距离
		selectHelper: false,
		selectEventOverlap: false, // 相同时间段的多个日程视觉上是否允许重叠，默认为true，允许
		select: this.handleDateSelect,
		timeGridEventMinHeight: '20', // 设置事件的最小高度
		weekNumberCalculation: 'ISO', // 与firstDay配套使用
        weekends: true,
		dayMaxEvents: true,
        eventClick: this.handleEventClick,
        eventsSet: this.handleEvents
        /* you can update a remote database when these fire:
        eventAdd:
        eventChange:
        eventRemove:
        */
      },
      currentEvents: [],
    }
  },
  methods: {
	fetchEvents(fetchInfo, successCallback, failureCallback) {
		const params = new URLSearchParams(window.location.search);
		const userid = params.get('userid');
		axios.get('http://localhost:5000/getUserEvent?userid=' + userid)
			.then(response => {
				let events = []
				response.data.forEach(event => {
					let start = this.parseDateTime(event.date,event.time,0);
					let end = this.parseDateTime(event.date,event.time,1);
	
					events.push({
						id: event.eventID,
						title: event.eventName,
						start: start,
						end: end,
						display: 'block', 
					})
				})
				successCallback(events)
			})
			.catch(error => {
				console.error('Error fetching events:', error);
			});
	},
	parseDateTime(dateday,dateTime,type) {
	    // 将'2024.05.02 21:45:56'转换为'2024-05-02T21:45:56'
		if(type == 0)
		{
			let date = dateday;
			let time = dateTime.split(' ')[type];
			return date + 'T' + time;
		}
	    
	},
    handleWeekendsToggle() {
      this.calendarOptions.weekends = !this.calendarOptions.weekends
    },
    handleDateSelect(selectInfo) {
      let title = prompt('Please enter a new title for your event')
      let calendarApi = selectInfo.view.calendar

      calendarApi.unselect()

      if (title) {
        calendarApi.addEvent({
          id: createEventId(),
          title,
          start: selectInfo.startStr,
          end: selectInfo.endStr,
          allDay: selectInfo.allDay
        })
      }
    },
    handleEventClick(clickInfo) {
      if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
        clickInfo.event.remove()
      }
    },
    handleEvents(events) {
      this.currentEvents = events
    },
  }
})

</script>

<style lang='css'>

.cal h2 {
  margin: 0px;
  font-size: 16px;
}

.cal ul {
  margin: 0;
  padding: 0 0 0 1.5em;
}

.cal-left li {
  margin: 1.5em 0;
  padding: 0;
}

.cal b {
  margin-right: 3px;
}

.cal {
  display: flex;
  min-height: 100%;
  font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
  font-size: 14px;
}

.cal-left {
  width: 22%;
  line-height: 1.5;
  background: #eaf9ff;
  border-right: 1px solid #d3e2e8;
}

.cal-left-label {
  padding-left: 2em;
  padding-up: 10px;
}
.cal-left-title {
  padding: 2em;
}
.cal-main {
  flex-grow: 1;
  padding: 3em;
}
.fc-event-main {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  
}


</style>
