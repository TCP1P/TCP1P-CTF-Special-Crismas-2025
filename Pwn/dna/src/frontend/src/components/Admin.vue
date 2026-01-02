<script setup>
import { ShieldAlert } from 'lucide-vue-next'
</script>

<template>
  <div class="max-w-2xl mx-auto mt-10">
    <div class="bg-red-950/10 border border-red-900/50 rounded-lg p-12 text-center relative overflow-hidden">
      <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImEiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTTAgNDBMODAgMCIgc3Ryb2tlPSIjNDUwMDAwIiBzdHJva2Utd2lkdGg9IjEiIGZpbGw9Im5vbmUiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjYSkiLz48L3N2Zz4=')] opacity-20 pointer-events-none"></div>

      <ShieldAlert class="w-16 h-16 text-red-600 mx-auto mb-6 opacity-80" />

      <h2 class="text-3xl font-bold text-red-500 mb-2 tracking-widest">RESTRICTED AREA</h2>

      <div class="inline-block bg-black/50 border border-red-900 p-4 rounded font-mono text-xs text-red-300">
        REQUIRED_ROLE: 0x1337C0DE<br>
        CURRENT_ROLE: GUEST (0x00000000)
      </div>
    </div>
  </div>
</template>
