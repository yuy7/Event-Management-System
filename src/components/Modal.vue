<template>
    <div class="modal">
        <div class="modal-content">
            <h2>{{ title }}</h2>
			<div class="pick">
				<slot></slot>
				<button class="close" @click="$emit('close')">关闭</button>
			</div>
            
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            title: String
        }
    }
</script>

<style scoped>
    /* Your modal styles here */
	.modal{
		margin-up:50px;
		margin-left:50px;
		padding :15px;
	}
	.close{
		padding: 3px 13px;
		font-size: 14px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease
	}
	.close:hover {
	  background-color: #595959;
	}
</style>
