<template>
    <div class="modal">
        <div class="modal-content">
            <h2>{{ title }}</h2>
			<div class="pick">
				<slot></slot>
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
	.close:hover {
	  background-color: #595959;
	}
</style>
