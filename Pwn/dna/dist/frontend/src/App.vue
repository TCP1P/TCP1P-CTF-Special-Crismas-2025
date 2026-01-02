<script setup>
import { ref } from 'vue'
import Shop from './components/Shop.vue'
import Profile from './components/Profile.vue'
import Admin from './components/Admin.vue'
import Status from './components/Status.vue' // New Distraction Component
import { ShoppingCart, User, ShieldAlert, Activity } from 'lucide-vue-next'

const view = ref('shop')

// Simple navigation function
const navigate = (target) => {
  view.value = target
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-[#050505] text-blue-500 font-mono selection:bg-blue-900 selection:text-white">
    <nav class="border-b border-blue-900/30 p-4 bg-black/90 flex flex-col md:flex-row justify-between items-center sticky top-0 z-50 backdrop-blur-md">
      <div class="flex items-center gap-3 mb-4 md:mb-0 cursor-pointer" @click="navigate('shop')">
        <div class="relative w-6 h-6 flex items-center justify-center">
          <div class="absolute inset-0 bg-blue-500 blur-md opacity-20 animate-pulse"></div>
          <div class="text-2xl">🧬</div>
        </div>
        <h1 class="text-xl font-bold tracking-[0.2em] text-gray-200">
          PROJECT <span class="text-blue-500">DNA</span>
        </h1>
      </div>

      <div class="flex gap-1 md:gap-6 text-xs md:text-sm bg-gray-900/50 p-1 rounded-lg border border-white/5">
        <button
          @click="navigate('shop')"
          :class="view==='shop' ? 'bg-blue-900/30 text-blue-400 border-blue-500/50 shadow-[0_0_10px_rgba(59,130,246,0.2)]' : 'text-gray-500 hover:text-gray-300'"
          class="flex gap-2 items-center px-4 py-2 rounded transition-all duration-300 border border-transparent">
          <ShoppingCart size="16"/> <span class="hidden sm:inline">SEQUENCE MARKET</span>
        </button>

        <button
          @click="navigate('profile')"
          :class="view==='profile' ? 'bg-blue-900/30 text-blue-400 border-blue-500/50 shadow-[0_0_10px_rgba(59,130,246,0.2)]' : 'text-gray-500 hover:text-gray-300'"
          class="flex gap-2 items-center px-4 py-2 rounded transition-all duration-300 border border-transparent">
          <User size="16"/> <span class="hidden sm:inline">INJECTOR UPLINK</span>
        </button>

        <button
          @click="navigate('status')"
          :class="view==='status' ? 'bg-blue-900/30 text-blue-400 border-blue-500/50 shadow-[0_0_10px_rgba(59,130,246,0.2)]' : 'text-gray-500 hover:text-gray-300'"
          class="flex gap-2 items-center px-4 py-2 rounded transition-all duration-300 border border-transparent">
          <Activity size="16"/> <span class="hidden sm:inline">SYS STATUS</span>
        </button>

        <button
          @click="navigate('admin')"
          :class="view==='admin' ? 'bg-red-900/20 text-red-500 border-red-500/50 shadow-[0_0_10px_rgba(239,68,68,0.2)]' : 'text-gray-500 hover:text-red-400'"
          class="flex gap-2 items-center px-4 py-2 rounded transition-all duration-300 border border-transparent">
          <ShieldAlert size="16"/> <span class="hidden sm:inline">CORE ACCESS</span>
        </button>
      </div>
    </nav>

    <main class="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full relative">
      <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCI+CjxwYXRoIGQ9Ik0wIDBoNDB2NDBIMHoiIGZpbGw9Im5vbmUiLz4KPHBhdGggZD0iTTAgNDBoNDBNNDAgMHY0MCIgc3Ryb2tlPSIjMWMxYzFjIiBzdHJva2Utb3BhY2l0eT0iMC4xIi8+Cjwvc3ZnPg==')] opacity-20 pointer-events-none"></div>

      <Transition name="fade" mode="out-in">
        <Shop v-if="view==='shop'" />
        <Profile v-else-if="view==='profile'" />
        <Admin v-else-if="view==='admin'" />
        <Status v-else-if="view==='status'" />
      </Transition>
    </main>

    <footer class="border-t border-gray-900 bg-black text-[10px] p-2 flex justify-between items-center text-gray-600 font-mono">
      <div class="flex gap-4">
        <span>NODE: <span class="text-green-900">ACTIVE</span></span>
        <span>LATENCY: <span class="animate-pulse text-blue-900">4ms</span></span>
      </div>
      <div>SECURE CONNECTION // TLS v1.3</div>
    </footer>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
