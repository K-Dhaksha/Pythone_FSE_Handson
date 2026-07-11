<template>
  <div class="course-card">
    <div class="card-header">
      <span class="course-code">{{ code }}</span>
      <span class="course-credits">{{ credits }} Credits</span>
    </div>
    <h3 class="course-name">{{ name }}</h3>
    <div class="card-footer">
      <span class="course-grade">Target Grade: <strong>{{ grade }}</strong></span>
      <div class="card-actions">
        <slot name="actions"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    required: true
  },
  code: {
    type: String,
    required: true
  },
  credits: {
    type: Number,
    required: true
  },
  grade: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
.course-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 16px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.course-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 0;
}

.course-card:hover {
  transform: translateY(-6px);
  border-color: rgba(168, 85, 247, 0.4);
  box-shadow: 0 12px 40px rgba(168, 85, 247, 0.15);
}

.course-card:hover::before {
  opacity: 1;
}

.card-header,
.course-name,
.card-footer {
  position: relative;
  z-index: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-code {
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #a855f7;
  background: rgba(168, 85, 247, 0.15);
  padding: 4px 10px;
  border-radius: 20px;
}

.course-credits {
  font-size: 0.85rem;
  font-weight: 500;
  color: #9ca3af;
}

.course-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #f3f4f6;
  margin: 0;
  line-height: 1.4;
  height: 56px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  padding-top: 12px;
}

.course-grade {
  font-size: 0.9rem;
  color: #9ca3af;
}

.course-grade strong {
  color: #34d399;
  font-weight: 600;
}

.card-actions {
  display: flex;
  width: 100%;
}
</style>
