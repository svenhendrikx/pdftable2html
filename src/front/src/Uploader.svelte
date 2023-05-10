<script>
    import { writable } from 'svelte/store';
    import Table from './Table.svelte';

    
    let files;
    let error = '';
    let pages;
    let tableData;

    const validatePages = () => {
        if (pages) {
            let regex = /^(\d+,)*\d+$/;

            return regex.test(pages);

        } else {
            return false
        }
    }
    const uploadFile = async () => {
        if (!files) {
            error = "Please specify a file"
            return 
        }
        if (!validatePages()) {
            error = 'pages should be a comma separated list of page numbers'
            return
        }
        error = '';

        const formData = new FormData();
        formData.append("file", files[0]);
        formData.append("pages", pages);

        const response = await fetch("/convert", {
            method: "POST",
            body: formData,
        });

        const text = await response.json();
        tableData = text;
        console.log(tableData)
    };
</script>
<style>
    .error {
        border: 2px solid red;
        background-color: #FFCCCC;
        color: red;
        padding: 10px;
        margin: 10px;
        border-radius: 5px;
        font-size: 14px;
    }
</style>
{#if error}
    <div class='error'>{error}</div><br>
{/if}
<input type="text" bind:value={pages}><br>
<input type="file" bind:files={files} accept=".pdf"><br>
<button on:click={uploadFile}>Upload</button>

{#if tableData}
    <Table {tableData} />
    <br>
{/if}
