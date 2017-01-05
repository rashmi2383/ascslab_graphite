#ifndef __PIN_CONFIG_H__
#define __PIN_CONFIG_H__

#include "fixed_types.h"

class PinConfig
{
   public:
      class StackAttributes
      {
         public:
            IntPtr lower_limit;
            UInt32 size;
      };

   public:

      static PinConfig *getSingleton();
      static void allocate();
      static void release();

      // Since Pin messes with stack, we need to handle that separately
      IntPtr getStackLowerLimit() const
      { return m_stack_lower_limit; }
      IntPtr getStackUpperLimit() const
      { return m_stack_upper_limit; }
      UInt32 getStackSizePerCore() const
      { return m_stack_size_per_core; }

      UInt32 getMaxThreadsPerCore() const
      { return m_max_threads_per_core; }

      tile_id_t getTileIDFromStackPtr(IntPtr stack_ptr);
      core_id_t getCoreIDFromStackPtr(IntPtr stack_ptr);
      thread_id_t getThreadIDFromStackPtr(IntPtr stack_ptr);
      SInt32 getStackAttributesFromCoreID (core_id_t core_id, StackAttributes& stack_attr);
      SInt32 getStackAttributesFromCoreAndThreadID (core_id_t core_id, thread_id_t thread_id, StackAttributes& stack_attr);

   private:

      // I think this should be private to have a 
      // true singleton
      PinConfig();
      ~PinConfig();

      // Pin specific variables
      UInt32 m_current_process_num;
      UInt32 m_total_tiles;
      UInt32 m_num_local_tiles;
      UInt32 m_max_threads_per_core;

      IntPtr m_stack_lower_limit;
      UInt32 m_stack_size_per_core;
      IntPtr m_stack_upper_limit;

      static PinConfig *m_singleton;

      void setStackBoundaries();
};

#endif
