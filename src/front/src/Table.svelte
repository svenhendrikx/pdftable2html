<script>
    export let tableData;
</script>

<svelte:head>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
    </style>
</svelte:head>

{#each tableData as table}
    {@html table.body}
{/each}
