<template>
    <h5 class="uk-margin-remove-top uk-text-bold uk-margin-small-bottom">
        Serial Read
    </h5>
    <ul>
        <li v-for="(event, index) in events" :key="index">{{ event }}</li>
    </ul>
</template>

<script>
export default {
    data() {
        return {
            events: []
        };
    },
    mounted() {
        // Replace 'YOUR_EVENT_SOURCE_URL' with the actual URL of your EventSource stream
        const eventSource = new EventSource('/serial_data');

        eventSource.onmessage = (event) => {
            // Update the events array with the new event data
            this.events.push(event.data);
        };

        eventSource.onerror = (error) => {
            console.error('EventSource failed:', error);
            eventSource.close();
        };
    },
    beforeUnmount() {
        // Close the EventSource connection when the component is unmounted
        eventSource.close();
    }
};
</script>