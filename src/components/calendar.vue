<template>
	<navbar></navbar>
	<div class='cal'>
		<div class='cal-left'>
			<div class='cal-left-title'>
				<h2>欢迎来到活动管理系统！</h2>
			</div>
			<div class='cal-left-label'>
				<label>
					<input type='checkbox' :checked='calendarOptions.weekends' @change='handleWeekendsToggle' />
					是否显示周末
				</label>
			</div>
			<div class='cal-left-title'>
				<h2>所有活动安排({{ currentEvents.length }})</h2>
				<ul>
					<li v-for='event in currentEvents' :key='event.id'>
						{{ event.title }}
					</li>
				</ul>
			</div>
		</div>
		<div class='cal-main'>
			<FullCalendar class='cal-calendar' :options='calendarOptions'>
				<template v-slot:eventContent='arg'>
					<b :style="{ color: getTextColor(arg.event.extendedProps.eventTypeID) }">{{ arg.timeText }}</b>
					<span
						:style="{ color: getTextColor(arg.event.extendedProps.eventTypeID) }">{{ arg.event.title }}</span>
				</template>
			</FullCalendar>
		</div>
	</div>
</template>


<script>
	import {
		defineComponent
	} from 'vue'
	import FullCalendar from '@fullcalendar/vue3'
	import dayGridPlugin from '@fullcalendar/daygrid'
	import timeGridPlugin from '@fullcalendar/timegrid'
	import interactionPlugin from '@fullcalendar/interaction'
	import {
		INITIAL_EVENTS,
		createEventId
	} from './event-utils'
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
			getTextColor(eventTypeID) {
				console.log(eventTypeID);
				switch (eventTypeID) {
					case 0:
					case 1:
					case 4:
						return '#a1d7f2';
					case 2:
					case 3:
					case 5:
						return '#a6e58e';
					case 6:
						return '#edbbf9';
					case 7:
						return '#f0bf71';
					default:
						return '#000000'; // 默认颜色
				}
			},
			fetchEvents(fetchInfo, successCallback, failureCallback) {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get('userid');
				axios.get('http://localhost:5000/getUserAllEvent?userid=' + userid)
					.then(response => {
						console.log(response.data);
						let events = []
						response.data.forEach(event => {
							let start = this.parseDateTime(event.date, event.time, 0);
							let end = this.parseDateTime(event.date, event.time, 1);
							let color;
							switch (event.eventTypeID) {
								case 0:
								case 1:
								case 4:
									color = '#D1EFFE';
									break;
								case 2:
								case 3:
								case 5:
									color = '#E0F8D7';
									break;
								case 6:
									color = '#F5E4F9';
									break;
								case 7:
									color = '#FEEACA';
									break;
							}
							events.push({
								id: event.eventID,
								title: event.eventName,
								start: start,
								end: end,
								display: 'block',
								backgroundColor: color,
								borderColor: color,
								extendedProps: {
								  eventTypeID: event.eventTypeID
								}
							})

						})
						console.log(events);
						successCallback(events);
						this.handleEvents(events);
					})
					.catch(error => {
						console.error('Error fetching events:', error);
					});
			},
			parseDateTime(dateday, dateTime, type) {
				let date = dateday;
				let timeParts = dateTime.split('-')[type].split(':');
				let hours = timeParts[0].padStart(2, '0');
				let minutes = timeParts[1].padStart(2, '0');
				// let seconds = timeParts[2].padStart(2, '0');
				return date + 'T' + hours + ':' + minutes + ':00';
			},
			handleWeekendsToggle() {
				this.calendarOptions.weekends = !this.calendarOptions.weekends
			},
			handleDateSelect(selectInfo) {
				let title = prompt('请输入你的私人行程名称：')
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
				if (confirm(`你确定要删除活动'${clickInfo.event.title}'吗`)) {

					console.log(clickInfo.event.id);
					axios.post('http://localhost:5000/deleteEvent', {
							eventID: clickInfo.event.id
						})
						.then(response => {
							console.log('Response:', response.data);
							clickInfo.event.remove()
							alert('活动删除成功');
						})
						.catch(error => {
							console.error('Error approving message:', error);
							alert('活动删除失败，请重试');
						});
				}
			},
			handleEvents(events) {
				this.currentEvents = events
				console.log(this.currentEvents)
			},
		}
	})
</script>

<style lang='css'>
    body {
        background-color: #ecf0f3; /* 更改主背景色为蓝色 */
    }

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
        width: 17%;
        line-height: 1.5;
        border-right: 1px solid grey;
        background-color: #ffffff; /* 更改卡片背景色为白色 */
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* 添加阴影效果 */
        transition: 0.3s; /* 添加过渡效果 */
        border-radius: 15px; /* 设置圆角背景 */
		margin:15px;
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
		border-right: 1px solid grey;
        background-color: #ffffff; /* 更改卡片背景色为白色 */
        border-radius: 15px; /* 设置圆角背景 */
		margin:15px;
		box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* 添加阴影效果 */
		transition: 0.3s; /* 添加过渡效果 */
    }

    .fc-event-main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
</style>